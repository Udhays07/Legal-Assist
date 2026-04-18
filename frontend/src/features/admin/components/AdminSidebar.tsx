"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Separator } from "@/components/ui/separator";
import { LayoutDashboard, Tag, FileText, Scale, LogOut } from "lucide-react";
import { cn } from "@/lib/utils";
import { clearAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";

interface NavItem {
  label: string;
  href: string;
  icon: React.ElementType;
}

const navItems: NavItem[] = [
  { label: "Dashboard", href: "/admin", icon: LayoutDashboard },
  { label: "Categories", href: "/admin/categories", icon: Tag },
  { label: "Documents", href: "/admin/documents", icon: FileText },
];

export default function AdminSidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    clearAuth();
    router.push("/");
  };

  return (
    <aside className="w-[240px] shrink-0 flex flex-col sticky top-0 h-screen overflow-y-auto bg-card border-r border-border backdrop-blur-xl px-3 py-5 gap-1">
      {/* Brand */}
      <div className="flex items-center gap-3 px-3 pb-4">
        <div className="w-9 h-9 rounded-[10px] bg-gradient-to-br from-[#3b82f6] to-[#8b5cf6] flex items-center justify-center text-white shrink-0 shadow-[0_0_14px_rgba(59,130,246,0.4)]">
          <Scale size={18} />
        </div>
        <div className="flex flex-col">
          <span className="font-bold text-[0.95rem] font-[family-name:var(--font-display)] text-foreground leading-tight">
            S8 Legal
          </span>
          <span className="text-[0.68rem] text-muted-foreground uppercase tracking-widest">
            Admin Panel
          </span>
        </div>
      </div>

      <Separator className="bg-border mb-2" />

      {/* Nav */}
      <nav className="flex flex-col gap-0.5 flex-1">
        <p className="text-[0.65rem] font-semibold uppercase tracking-[0.1em] text-muted-foreground px-3 pb-1.5 pt-1">
          Main
        </p>
        {navItems.map(({ label, href, icon: Icon }) => {
          const isActive =
            href === "/admin" ? pathname === "/admin" : pathname.startsWith(href);

          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-[10px] text-sm font-medium transition-all duration-150 relative group",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <Icon size={17} className="shrink-0 opacity-85" />
              <span className="flex-1">{label}</span>
              {isActive && (
                <span className="absolute right-2 w-1 h-4 rounded-full bg-primary" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="flex flex-col gap-2 mt-auto">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-3 py-2.5 rounded-[10px] text-sm font-medium text-destructive hover:bg-destructive/10 transition-all duration-150 group"
        >
          <LogOut size={17} className="shrink-0 opacity-85 group-hover:translate-x-0.5 transition-transform" />
          <span className="flex-1 text-left">Logout</span>
        </button>
        <Separator className="bg-border" />
        <p className="text-[0.68rem] text-muted-foreground text-center opacity-40 py-1">
          S8 Legal Solutions © 2026
        </p>
      </div>
    </aside>
  );
}
