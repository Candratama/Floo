"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Card } from "@/components/ui/card";
import {
  LayoutDashboard,
  Receipt,
  Tags,
  Building2,
  User,
  Banana,
} from "lucide-react";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Transactions", href: "/dashboard/transactions", icon: Receipt },
  { name: "Categories", href: "/dashboard/categories", icon: Tags },
  { name: "Banks", href: "/dashboard/banks", icon: Building2 },
  { name: "Profile", href: "/dashboard/profile", icon: User },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <Card className="h-full w-64 px-3 py-4 border-r">
      <div className="space-y-4">
        <div className="flex items-center gap-2 px-4">
          <div className="flex p-2 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <Banana size={24} />
          </div>
          <h2 className="text-2xl font-bold">FLOO</h2>
        </div>
        <div className="px-3 py-2">
          <div className="space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:text-primary ${
                    isActive
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:bg-primary/5"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </Card>
  );
}
