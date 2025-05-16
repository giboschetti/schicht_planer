import { FilterBar } from "@/components/filter-bar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// Beispieldaten für den Wochenplan
const weekData = [
  {
    time: "06:00 - 14:00",
    name: "Frühschicht",
    days: [
      { date: "Mo, 01.05", workers: ["Thomas Müller", "Lisa Schmidt", "Michael Weber", "Anna Becker", "Jan Hoffmann"] },
      { date: "Di, 02.05", workers: ["Thomas Müller", "Lisa Schmidt", "Michael Weber", "Anna Becker"] },
      {
        date: "Mi, 03.05",
        workers: ["Thomas Müller", "Lisa Schmidt", "Michael Weber", "Anna Becker", "Jan Hoffmann", "Sarah Koch"],
      },
      { date: "Do, 04.05", workers: ["Thomas Müller", "Lisa Schmidt", "Michael Weber"] },
      { date: "Fr, 05.05", workers: ["Thomas Müller", "Lisa Schmidt"] },
      { date: "Sa, 06.05", workers: [] },
      { date: "So, 07.05", workers: [] },
    ],
  },
  {
    time: "14:00 - 22:00",
    name: "Spätschicht",
    days: [
      { date: "Mo, 01.05", workers: ["Klaus Wagner", "Petra Schulz", "Martin Fischer"] },
      { date: "Di, 02.05", workers: ["Klaus Wagner", "Petra Schulz", "Martin Fischer", "Sandra Bauer"] },
      { date: "Mi, 03.05", workers: ["Klaus Wagner", "Petra Schulz"] },
      {
        date: "Do, 04.05",
        workers: ["Klaus Wagner", "Petra Schulz", "Martin Fischer", "Sandra Bauer", "Robert Krause"],
      },
      { date: "Fr, 05.05", workers: [] },
      { date: "Sa, 06.05", workers: [] },
      { date: "So, 07.05", workers: [] },
    ],
  },
]

export default function WeekView() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Wochenansicht</h1>

      <FilterBar />

      <Card>
        <CardHeader>
          <CardTitle>KW 18 (01.05 - 07.05.2025)</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            {weekData.map((shift, index) => (
              <div key={index} className="mb-6">
                <h3 className="font-medium mb-2">
                  {shift.name} ({shift.time})
                </h3>
                <Table>
                  <TableHeader>
                    <TableRow>
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
                    <TableRow>
                      {shift.days.map((day, dayIndex) => (
                        <TableCell key={dayIndex} className="align-top">
                          <div className="text-xs font-medium mb-1">{day.date.split(", ")[1]}</div>
                          {day.workers.length > 0 ? (
                            <ul className="text-xs space-y-1">
                              {day.workers.map((worker, workerIndex) => (
                                <li key={workerIndex} className="bg-muted p-1 rounded">
                                  {worker}
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <div className="text-xs text-muted-foreground italic">Keine Schicht</div>
                          )}
                        </TableCell>
                      ))}
                    </TableRow>
                  </TableBody>
                </Table>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
