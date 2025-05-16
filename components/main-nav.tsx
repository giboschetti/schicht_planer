"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Calendar, CalendarDays, CalendarRange, Clipboard, Menu } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"

export function MainNav() {
  const pathname = usePathname()

  const routes = [
    {
      href: "/monatsansicht",
      label: "Monatsansicht",
      icon: <Calendar className="h-5 w-5 mr-2" />,
      active: pathname === "/monatsansicht",
    },
    {
      href: "/wochenansicht",
      label: "Wochenansicht",
      icon: <CalendarRange className="h-5 w-5 mr-2" />,
      active: pathname === "/wochenansicht",
    },
    {
      href: "/tagesansicht",
      label: "Tagesansicht",
      icon: <CalendarDays className="h-5 w-5 mr-2" />,
      active: pathname === "/tagesansicht",
    },
    {
      href: "/schichtdetails",
      label: "Schichtdetails",
      icon: <Clipboard className="h-5 w-5 mr-2" />,
      active: pathname === "/schichtdetails",
    },
  ]

  return (
    <div className="flex items-center">
      {/* Mobile Navigation */}
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="outline" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
            <span className="sr-only">Menü öffnen</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left">
          <div className="flex flex-col gap-4 mt-8">
            {routes.map((route) => (
              <Link
                key={route.href}
                href={route.href}
                className={cn(
                  "flex items-center text-lg font-medium transition-colors hover:text-primary",
                  route.active ? "text-primary" : "text-muted-foreground",
                )}
              >
                {route.icon}
                {route.label}
              </Link>
            ))}
          </div>
        </SheetContent>
      </Sheet>

      {/* Desktop Navigation */}
      <nav className="hidden md:flex items-center space-x-4 lg:space-x-6">
        {routes.map((route) => (
          <Link
            key={route.href}
            href={route.href}
            className={cn(
              "flex items-center text-sm font-medium transition-colors hover:text-primary",
              route.active ? "text-primary" : "text-muted-foreground",
            )}
          >
            {route.icon}
            {route.label}
          </Link>
        ))}
      </nav>
    </div>
  )
}
