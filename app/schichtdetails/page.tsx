import { FilterBar } from "@/components/filter-bar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

// Beispieldaten für die Schichtdetails
const shiftDetails = {
  date: "01.05.2025",
  shift: {
    name: "Frühschicht",
    time: "06:00 - 14:00",
    manager: "Thomas Müller",
    managerContact: "+49 123 456789",
    sectors: [
      {
        name: "Nordsektor",
        tasks: [
          { id: "N1", description: "Fundament gießen", status: "In Bearbeitung", assignedTo: "Lisa Schmidt" },
          { id: "N2", description: "Stahlträger montieren", status: "Geplant", assignedTo: "Michael Weber" },
        ],
        workers: [
          { name: "Lisa Schmidt", role: "Kranführer", hours: 8, notes: "Kranführerschein erneuert" },
          { name: "Michael Weber", role: "Maurer", hours: 8, notes: "" },
        ],
      },
      {
        name: "Südsektor",
        tasks: [
          { id: "S1", description: "Elektroinstallation", status: "In Bearbeitung", assignedTo: "Anna Becker" },
          { id: "S2", description: "Mauerwerk errichten", status: "Geplant", assignedTo: "Jan Hoffmann" },
        ],
        workers: [
          { name: "Anna Becker", role: "Elektriker", hours: 8, notes: "Spezialist für Industrieverkabelung" },
          { name: "Jan Hoffmann", role: "Maurer", hours: 8, notes: "" },
        ],
      },
    ],
    equipment: [
      { name: "Bagger", id: "B-123", assignedTo: "Nordsektor" },
      { name: "Kran", id: "K-456", assignedTo: "Nordsektor" },
      { name: "Betonmischer", id: "BM-789", assignedTo: "Südsektor" },
    ],
    notes: "Wetterbericht: Sonnig, 18°C. Lieferung von Baumaterial um 10:00 Uhr erwartet.",
  },
}

export default function ShiftDetails() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Schichtdetails</h1>

      <FilterBar />

      <Card>
        <CardHeader>
          <div className="flex flex-wrap items-center gap-2">
            <CardTitle>{shiftDetails.shift.name}</CardTitle>
            <Badge variant="outline">{shiftDetails.shift.time}</Badge>
            <Badge>{shiftDetails.date}</Badge>
          </div>
          <div className="flex items-center gap-2 mt-2">
            <Avatar className="h-8 w-8">
              <AvatarFallback>
                {shiftDetails.shift.manager
                  .split(" ")
                  .map((n) => n[0])
                  .join("")}
              </AvatarFallback>
            </Avatar>
            <div>
              <div className="font-medium">{shiftDetails.shift.manager}</div>
              <div className="text-sm text-muted-foreground">{shiftDetails.shift.managerContact}</div>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="sectors">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="sectors">Sektoren</TabsTrigger>
              <TabsTrigger value="tasks">Aufgaben</TabsTrigger>
              <TabsTrigger value="workers">Mitarbeiter</TabsTrigger>
              <TabsTrigger value="equipment">Ausrüstung</TabsTrigger>
            </TabsList>

            <TabsContent value="sectors" className="space-y-4 mt-4">
              {shiftDetails.shift.sectors.map((sector, index) => (
                <Card key={index}>
                  <CardHeader>
                    <CardTitle>{sector.name}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-medium mb-2">Mitarbeiter</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                          {sector.workers.map((worker, workerIndex) => (
                            <div key={workerIndex} className="flex items-center p-2 border rounded-md">
                              <div>
                                <div className="font-medium">{worker.name}</div>
                                <div className="text-sm text-muted-foreground">{worker.role}</div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div>
                        <h4 className="font-medium mb-2">Aufgaben</h4>
                        <div className="space-y-2">
                          {sector.tasks.map((task, taskIndex) => (
                            <div key={taskIndex} className="p-2 border rounded-md">
                              <div className="flex justify-between">
                                <div className="font-medium">
                                  {task.id}: {task.description}
                                </div>
                                <Badge variant={task.status === "Geplant" ? "outline" : "default"}>{task.status}</Badge>
                              </div>
                              <div className="text-sm text-muted-foreground">Zugewiesen an: {task.assignedTo}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </TabsContent>

            <TabsContent value="tasks" className="space-y-4 mt-4">
              <div className="space-y-2">
                {shiftDetails.shift.sectors.flatMap((sector) =>
                  sector.tasks.map((task, taskIndex) => (
                    <Card key={`${sector.name}-${taskIndex}`}>
                      <CardContent className="p-4">
                        <div className="flex justify-between items-center">
                          <div>
                            <div className="font-medium">
                              {task.id}: {task.description}
                            </div>
                            <div className="text-sm text-muted-foreground">
                              Sektor: {sector.name} | Zugewiesen an: {task.assignedTo}
                            </div>
                          </div>
                          <Badge variant={task.status === "Geplant" ? "outline" : "default"}>{task.status}</Badge>
                        </div>
                      </CardContent>
                    </Card>
                  )),
                )}
              </div>
            </TabsContent>

            <TabsContent value="workers" className="mt-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {shiftDetails.shift.sectors.flatMap((sector) =>
                  sector.workers.map((worker, workerIndex) => (
                    <Card key={`${sector.name}-${workerIndex}`}>
                      <CardContent className="p-4">
                        <div className="flex items-center gap-4">
                          <Avatar className="h-10 w-10">
                            <AvatarFallback>
                              {worker.name
                                .split(" ")
                                .map((n) => n[0])
                                .join("")}
                            </AvatarFallback>
                          </Avatar>
                          <div>
                            <div className="font-medium">{worker.name}</div>
                            <div className="text-sm">{worker.role}</div>
                            <div className="text-sm text-muted-foreground">Sektor: {sector.name}</div>
                            <div className="text-sm text-muted-foreground">Stunden: {worker.hours}</div>
                            {worker.notes && <div className="text-sm italic mt-1">{worker.notes}</div>}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  )),
                )}
              </div>
            </TabsContent>

            <TabsContent value="equipment" className="mt-4">
              <div className="space-y-2">
                {shiftDetails.shift.equipment.map((item, index) => (
                  <Card key={index}>
                    <CardContent className="p-4">
                      <div className="flex justify-between items-center">
                        <div>
                          <div className="font-medium">{item.name}</div>
                          <div className="text-sm text-muted-foreground">
                            ID: {item.id} | Zugewiesen an: {item.assignedTo}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>
          </Tabs>

          <div className="mt-6">
            <h4 className="font-medium mb-2">Notizen</h4>
            <div className="p-3 bg-muted rounded-md">{shiftDetails.shift.notes}</div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
