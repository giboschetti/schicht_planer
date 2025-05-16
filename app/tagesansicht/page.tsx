import { FilterBar } from "@/components/filter-bar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

// Beispieldaten für den Tagesplan
const dayData = {
  date: "01.05.2025",
  shifts: [
    {
      name: "Frühschicht",
      time: "06:00 - 14:00",
      manager: "Thomas Müller",
      workers: [
        { name: "Lisa Schmidt", sector: "Nordsektor", role: "Kranführer" },
        { name: "Michael Weber", sector: "Nordsektor", role: "Maurer" },
        { name: "Anna Becker", sector: "Südsektor", role: "Elektriker" },
        { name: "Jan Hoffmann", sector: "Südsektor", role: "Maurer" },
      ],
    },
    {
      name: "Spätschicht",
      time: "14:00 - 22:00",
      manager: "Klaus Wagner",
      workers: [
        { name: "Petra Schulz", sector: "Nordsektor", role: "Kranführer" },
        { name: "Martin Fischer", sector: "Nordsektor", role: "Maurer" },
        { name: "Sandra Bauer", sector: "Südsektor", role: "Elektriker" },
      ],
    },
  ],
}

export default function DayView() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Tagesansicht</h1>

      <FilterBar />

      <Card>
        <CardHeader>
          <CardTitle>Donnerstag, {dayData.date}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {dayData.shifts.map((shift, index) => (
              <div key={index} className="space-y-3">
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="text-lg font-medium">{shift.name}</h3>
                  <Badge variant="outline">{shift.time}</Badge>
                  <div className="text-sm text-muted-foreground">
                    Schichtleiter: <span className="font-medium">{shift.manager}</span>
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Mitarbeiter</TableHead>
                        <TableHead>Sektor</TableHead>
                        <TableHead>Rolle</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {shift.workers.map((worker, workerIndex) => (
                        <TableRow key={workerIndex}>
                          <TableCell className="font-medium">{worker.name}</TableCell>
                          <TableCell>{worker.sector}</TableCell>
                          <TableCell>{worker.role}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
