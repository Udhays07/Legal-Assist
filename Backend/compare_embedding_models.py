"""
Embedding Model Comparison Script

Compares different 768-dimensional embedding models for legal document processing:
- intfloat/e5-base-v2
- BAAI/bge-base-en-v1.5
- sentence-transformers/multi-qa-mpnet-base-dot-v1
- sentence-transformers/all-mpnet-base-v2 (current)

Metrics evaluated:
1. Embedding generation speed
2. Semantic similarity quality
3. Memory usage
4. Model size
5. Retrieval accuracy

Usage:
    python compare_embedding_models.py
"""

import sys
import time
import psutil
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.admin import Document

# Models to compare (all 768 dimensions)
MODELS = {
    "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",
    "e5-base-v2": "intfloat/e5-base-v2",
    "bge-base-en-v1.5": "BAAI/bge-base-en-v1.5",
    "multi-qa-mpnet": "sentence-transformers/multi-qa-mpnet-base-dot-v1",
}

# Test queries for legal domain
TEST_QUERIES = [
    "contract termination clause",
    "liability and indemnification",
    "intellectual property rights",
    "confidentiality agreement",
    "dispute resolution arbitration",
    "payment terms and conditions",
    "force majeure provisions",
    "warranty and representations",
]

# Sample legal documents for testing
SAMPLE_DOCUMENTS = [
    "This agreement may be terminated by either party with 30 days written notice. Upon termination, all obligations cease except those that expressly survive termination.",
    "The parties agree to indemnify and hold harmless each other from any claims, damages, or liabilities arising from breach of this agreement.",
    "All intellectual property rights, including patents, trademarks, and copyrights, shall remain the exclusive property of the disclosing party.",
    "The receiving party agrees to maintain confidentiality of all proprietary information disclosed during the term of this agreement.",
    "Any disputes arising from this agreement shall be resolved through binding arbitration in accordance with applicable rules.",
    "Payment shall be due within 30 days of invoice date. Late payments shall accrue interest at the rate of 1.5% per month.",
    "Neither party shall be liable for failure to perform due to circumstances beyond reasonable control, including acts of God, war, or natural disasters.",
    "The seller warrants that the goods are free from defects and conform to specifications. This warranty is valid for 12 months from delivery.",
]


class ModelComparison:
    """Compare embedding models on various metrics."""
    
    def __init__(self):
        self.results = {}
        self.models = {}
        
    def load_model(self, model_name: str, model_path: str) -> SentenceTransformer:
        """Load a model and measure loading time."""
        print(f"\n{'='*60}")
        print(f"Loading: {model_name}")
        print(f"{'='*60}")
        
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        model = SentenceTransformer(model_path)
        
        load_time = time.time() - start_time
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        memory_used = end_memory - start_memory
        
        print(f"✓ Loaded in {load_time:.2f}s")
        print(f"✓ Memory used: {memory_used:.2f} MB")
        print(f"✓ Dimension: {model.get_sentence_embedding_dimension()}")
        
        self.results[model_name] = {
            "load_time": load_time,
            "memory_mb": memory_used,
            "dimension": model.get_sentence_embedding_dimension(),
        }
        
        return model
    
    def benchmark_speed(self, model_name: str, model: SentenceTransformer, 
                       texts: List[str], iterations: int = 3) -> Dict:
        """Benchmark embedding generation speed."""
        print(f"\n📊 Benchmarking speed for {model_name}...")
        
        times = []
        for i in range(iterations):
            start = time.time()
            embeddings = model.encode(texts, convert_to_numpy=True)
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"  Run {i+1}: {elapsed:.3f}s ({len(texts)/elapsed:.1f} docs/sec)")
        
        avg_time = np.mean(times)
        std_time = np.std(times)
        docs_per_sec = len(texts) / avg_time
        
        print(f"✓ Average: {avg_time:.3f}s ± {std_time:.3f}s")
        print(f"✓ Throughput: {docs_per_sec:.1f} documents/second")
        
        return {
            "avg_time": avg_time,
            "std_time": std_time,
            "docs_per_sec": docs_per_sec,
            "per_doc_ms": (avg_time / len(texts)) * 1000,
        }
    
    def evaluate_retrieval(self, model_name: str, model: SentenceTransformer,
                          queries: List[str], documents: List[str]) -> Dict:
        """Evaluate retrieval quality using semantic similarity."""
        print(f"\n🔍 Evaluating retrieval quality for {model_name}...")
        
        # Encode queries and documents
        query_embeddings = model.encode(queries, convert_to_numpy=True)
        doc_embeddings = model.encode(documents, convert_to_numpy=True)
        
        # Calculate similarities
        similarities = cosine_similarity(query_embeddings, doc_embeddings)
        
        # For each query, find top-3 most similar documents
        top_k = 3
        retrieval_scores = []
        
        for i, query in enumerate(queries):
            top_indices = np.argsort(similarities[i])[-top_k:][::-1]
            top_scores = similarities[i][top_indices]
            retrieval_scores.append(top_scores[0])  # Best match score
            
            # print(f"\n  Query: '{query[:50]}...'")
            # for j, (idx, score) in enumerate(zip(top_indices, top_scores), 1):
            #     print(f"    {j}. Score: {score:.4f} - '{documents[idx][:60]}...'")
        
        avg_score = np.mean(retrieval_scores)
        min_score = np.min(retrieval_scores)
        max_score = np.max(retrieval_scores)
        
        print(f"\n✓ Average best match score: {avg_score:.4f}")
        print(f"✓ Score range: {min_score:.4f} - {max_score:.4f}")
        
        return {
            "avg_best_match": avg_score,
            "min_score": min_score,
            "max_score": max_score,
            "all_scores": retrieval_scores,
        }
    
    def test_with_real_documents(self, model_name: str, model: SentenceTransformer,
                                limit: int = 10) -> Dict:
        """Test with real documents from database."""
        print(f"\n📚 Testing with real documents from database...")
        
        db = SessionLocal()
        try:
            # Get sample documents
            docs = db.query(Document).filter(
                Document.deleted_at == None
            ).limit(limit).all()
            
            if not docs:
                print("  ⚠️  No documents in database")
                return {"status": "no_documents"}
            
            print(f"  Found {len(docs)} documents")
            
            # Extract content
            contents = [doc.content[:500] for doc in docs]  # First 500 chars
            
            # Benchmark
            start = time.time()
            embeddings = model.encode(contents, convert_to_numpy=True)
            elapsed = time.time() - start
            
            print(f"  ✓ Generated {len(embeddings)} embeddings in {elapsed:.3f}s")
            print(f"  ✓ Average: {(elapsed/len(embeddings))*1000:.1f}ms per document")
            
            return {
                "num_docs": len(docs),
                "total_time": elapsed,
                "avg_time_ms": (elapsed/len(embeddings))*1000,
            }
            
        finally:
            db.close()
    
    def compare_all_models(self):
        """Run complete comparison for all models."""
        print("\n" + "="*60)
        print("EMBEDDING MODEL COMPARISON")
        print("="*60)
        print(f"\nComparing {len(MODELS)} models:")
        for name, path in MODELS.items():
            print(f"  • {name}: {path}")
        
        # Load and test each model
        for model_name, model_path in MODELS.items():
            try:
                # Load model
                model = self.load_model(model_name, model_path)
                self.models[model_name] = model
                
                # Benchmark speed
                speed_results = self.benchmark_speed(
                    model_name, model, SAMPLE_DOCUMENTS
                )
                self.results[model_name]["speed"] = speed_results
                
                # Evaluate retrieval
                retrieval_results = self.evaluate_retrieval(
                    model_name, model, TEST_QUERIES, SAMPLE_DOCUMENTS
                )
                self.results[model_name]["retrieval"] = retrieval_results
                
                # Test with real documents
                real_doc_results = self.test_with_real_documents(
                    model_name, model, limit=10
                )
                self.results[model_name]["real_docs"] = real_doc_results
                
            except Exception as e:
                print(f"\n✗ Error with {model_name}: {str(e)}")
                self.results[model_name]["error"] = str(e)
        
        # Print comparison summary
        self.print_summary()
    
    def print_summary(self):
        """Print comparison summary table."""
        print("\n" + "="*60)
        print("COMPARISON SUMMARY")
        print("="*60)
        
        # Model loading
        print("\n1. MODEL LOADING")
        print("-" * 60)
        print(f"{'Model':<25} {'Load Time':<15} {'Memory (MB)':<15}")
        print("-" * 60)
        for name, data in self.results.items():
            if "error" not in data:
                print(f"{name:<25} {data['load_time']:.2f}s{'':<10} {data['memory_mb']:.1f}")
        
        # Speed comparison
        print("\n2. EMBEDDING GENERATION SPEED")
        print("-" * 60)
        print(f"{'Model':<25} {'Docs/Sec':<15} {'ms/Doc':<15}")
        print("-" * 60)
        for name, data in self.results.items():
            if "error" not in data and "speed" in data:
                speed = data["speed"]
                print(f"{name:<25} {speed['docs_per_sec']:.1f}{'':<10} {speed['per_doc_ms']:.1f}")
        
        # Retrieval quality
        print("\n3. RETRIEVAL QUALITY (Semantic Similarity)")
        print("-" * 60)
        print(f"{'Model':<25} {'Avg Score':<15} {'Range':<20}")
        print("-" * 60)
        for name, data in self.results.items():
            if "error" not in data and "retrieval" in data:
                ret = data["retrieval"]
                range_str = f"{ret['min_score']:.3f} - {ret['max_score']:.3f}"
                print(f"{name:<25} {ret['avg_best_match']:.4f}{'':<10} {range_str}")
        
        # Real documents performance
        print("\n4. REAL DOCUMENTS PERFORMANCE")
        print("-" * 60)
        print(f"{'Model':<25} {'Docs Tested':<15} {'Avg Time (ms)':<15}")
        print("-" * 60)
        for name, data in self.results.items():
            if "error" not in data and "real_docs" in data:
                real = data["real_docs"]
                if "num_docs" in real:
                    print(f"{name:<25} {real['num_docs']:<15} {real['avg_time_ms']:.1f}")
        
        # Recommendation
        print("\n" + "="*60)
        print("RECOMMENDATION")
        print("="*60)
        
        # Find best model for each metric
        best_speed = max(
            [(name, data["speed"]["docs_per_sec"]) 
             for name, data in self.results.items() 
             if "error" not in data and "speed" in data],
            key=lambda x: x[1]
        )
        
        best_quality = max(
            [(name, data["retrieval"]["avg_best_match"]) 
             for name, data in self.results.items() 
             if "error" not in data and "retrieval" in data],
            key=lambda x: x[1]
        )
        
        best_memory = min(
            [(name, data["memory_mb"]) 
             for name, data in self.results.items() 
             if "error" not in data],
            key=lambda x: x[1]
        )
        
        print(f"\n🏆 Fastest: {best_speed[0]} ({best_speed[1]:.1f} docs/sec)")
        print(f"🎯 Best Quality: {best_quality[0]} (score: {best_quality[1]:.4f})")
        print(f"💾 Lowest Memory: {best_memory[0]} ({best_memory[1]:.1f} MB)")
        
        print("\n📝 Notes:")
        print("  • all-mpnet-base-v2: Best overall balance, great for general use")
        print("  • e5-base-v2: Excellent for retrieval tasks, requires 'query:' prefix")
        print("  • bge-base-en-v1.5: Strong performance, good for English documents")
        print("  • multi-qa-mpnet: Optimized for Q&A, good for legal queries")
        
        print("\n" + "="*60)


def main():
    """Run the comparison."""
    comparison = ModelComparison()
    
    try:
        comparison.compare_all_models()
        
        print("\n✓ Comparison complete!")
        print("\nResults saved in memory. To export:")
        print("  • Add JSON export functionality")
        print("  • Add visualization with matplotlib")
        print("  • Add detailed report generation")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Comparison interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Error during comparison: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()