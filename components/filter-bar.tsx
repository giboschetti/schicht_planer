"use client"

import { useState } from "react"
import { CalendarIcon, ChevronDown, Filter } from "lucide-react"
import { format } from "date-fns"
import { de } from "date-fns/locale"

import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"

// Beispieldaten für Filter
const schichtleiter = ["Alle Schichtleiter", "Thomas Müller", "Lisa Schmidt", "Michael Weber", "Anna Becker"]

const sektoren = ["Alle Sektoren", "Nordsektor", "Südsektor", "Ostsektor", "Westsektor"]

export function FilterBar() {
  const [date, setDate] = useState<Date | undefined>(new Date())
  const [selectedSchichtleiter, setSelectedSchichtleiter] = useState(schichtleiter[0])
  const [selectedSektor, setSelectedSektor] = useState(sektoren[0])

  return (
    <div className="flex flex-wrap items-center gap-2 p-2 bg-muted/40 rounded-lg">
      {/* Desktop Filters */}
      <div className="hidden md:flex items-center gap-2 w-full md:w-auto">
        <Popover>
          <PopoverTrigger asChild>
            <Button variant="outline" className="justify-start text-left font-normal w-[240px]">
              <CalendarIcon className="mr-2 h-4 w-4" />
              {date ? format(date, "PPP", { locale: de }) : "Datum auswählen"}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-0">
            <Calendar mode="single" selected={date} onSelect={setDate} locale={de} />
          </PopoverContent>
        </Popover>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="w-[200px] justify-between">
              {selectedSchichtleiter}
              <ChevronDown className="ml-2 h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            {schichtleiter.map((name) => (
              <DropdownMenuItem key={name} onClick={() => setSelectedSchichtleiter(name)}>
                {name}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="w-[180px] justify-between">
              {selectedSektor}
              <ChevronDown className="ml-2 h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            {sektoren.map((sektor) => (
              <DropdownMenuItem key={sektor} onClick={() => setSelectedSektor(sektor)}>
                {sektor}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {/* Mobile Filter Button */}
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="outline" className="md:hidden w-full">
            <Filter className="mr-2 h-4 w-4" />
            Filter
          </Button>
        </SheetTrigger>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Filter</SheetTitle>
          </SheetHeader>
          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <h4 className="font-medium">Datum</h4>
              <Calendar mode="single" selected={date} onSelect={setDate} locale={de} className="rounded-md border" />
            </div>
            <div className="space-y-2">
              <h4 className="font-medium">Schichtleiter</h4>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" className="w-full justify-between">
                    {selectedSchichtleiter}
                    <ChevronDown className="ml-2 h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  {schichtleiter.map((name) => (
                    <DropdownMenuItem key={name} onClick={() => setSelectedSchichtleiter(name)}>
                      {name}
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
            <div className="space-y-2">
              <h4 className="font-medium">Sektor</h4>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" className="w-full justify-between">
                    {selectedSektor}
                    <ChevronDown className="ml-2 h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  {sektoren.map((sektor) => (
                    <DropdownMenuItem key={sektor} onClick={() => setSelectedSektor(sektor)}>
                      {sektor}
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </SheetContent>
      </Sheet>
    </div>
  )
}
