import { FilterBar } from "@/components/filter-bar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// Beispieldaten für den Monatsplan
const monthData = [
  {
    week: 1,
    days: [
      {
        date: "01.05",
        shifts: [
          { name: "Frühschicht", workers: 5 },
          { name: "Spätschicht", workers: 3 },
        ],
      },
      {
        date: "02.05",
        shifts: [
          { name: "Frühschicht", workers: 4 },
          { name: "Spätschicht", workers: 4 },
        ],
      },
      {
        date: "03.05",
        shifts: [
          { name: "Frühschicht", workers: 6 },
          { name: "Spätschicht", workers: 2 },
        ],
      },
      {
        date: "04.05",
        shifts: [
          { name: "Frühschicht", workers: 3 },
          { name: "Spätschicht", workers: 5 },
        ],
      },
      {
        date: "05.05",
        shifts: [
          { name: "Frühschicht", workers: 2 },
          { name: "Spätschicht", workers: 0 },
        ],
      },
      {
        date: "06.05",
        shifts: [
          { name: "Frühschicht", workers: 0 },
          { name: "Spätschicht", workers: 0 },
        ],
      },
      {
        date: "07.05",
        shifts: [
          { name: "Frühschicht", workers: 0 },
          { name: "Spätschicht", workers: 0 },
        ],
      },
    ],
  },
  {
    week: 2,
    days: [
      {
        date: "08.05",
        shifts: [
          { name: "Frühschicht", workers: 5 },
          { name: "Spätschicht", workers: 4 },
        ],
      },
      {
        date: "09.05",
        shifts: [
          { name: "Frühschicht", workers: 6 },
          { name: "Spätschicht", workers: 3 },
        ],
      },
      {
        date: "10.05",
        shifts: [
          { name: "Frühschicht", workers: 4 },
          { name: "Spätschicht", workers: 4 },
        ],
      },
      {
        date: "11.05",
        shifts: [
          { name: "Frühschicht", workers: 5 },
          { name: "Spätschicht", workers: 3 },
        ],
      },
      {
        date: "12.05",
        shifts: [
          { name: "Frühschicht", workers: 3 },
          { name: "Spätschicht", workers: 0 },
        ],
      },
      {
        date: "13.05",
        shifts: [
          { name: "Frühschicht", workers: 0 },
          { name: "Spätschicht", workers: 0 },
        ],
      },
      {
        date: "14.05",
        shifts: [
          { name: "Frühschicht", workers: 0 },
          { name: "Spätschicht", workers: 0 },
        ],
      },
    ],
  },
]

export default function MonthView() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Monatsansicht</h1>

      <FilterBar />

      <Card>
        <CardHeader>
          <CardTitle>Mai 2025</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[100px]">KW</TableHead>
                  <TableHead>Mo</TableHead>
                  <TableHead>Di</TableHead>
                  <TableHead>Mi</TableHead>
                  <TableHead>Do</TableHead>
                  <TableHead>Fr</TableHead>
                  <TableHead>Sa</TableHead>
                  <TableHead>So</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {monthData.map((week) => (
                  <TableRow key={week.week}>
                    <TableCell className="font-medium">{week.week}</TableCell>
                    {week.days.map((day, index) => (
                      <TableCell key={index} className="p-2">
                        <div className="text-xs font-medium">{day.date}</div>
                        {day.shifts.map((shift, shiftIndex) => (
                          <div
                            key={shiftIndex}
                            className={`mt-1 p-1 text-xs rounded ${
                              shift.name === "Frühschicht"
                                ? "bg-blue-100 dark:bg-blue-950"
                                : "bg-amber-100 dark:bg-amber-950"
                            } ${shift.workers === 0 ? "opacity-30" : ""}`}
                          >
                            {shift.name}: {shift.workers}
                          </div>
                        ))}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
