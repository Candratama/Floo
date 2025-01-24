import { Card } from "@/components/ui/card";

export default function Dashboard() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="p-6">
          <h3 className="font-semibold">Total Transactions</h3>
          <p className="text-3xl font-bold">0</p>
        </Card>
        <Card className="p-6">
          <h3 className="font-semibold">Categories</h3>
          <p className="text-3xl font-bold">0</p>
        </Card>
        <Card className="p-6">
          <h3 className="font-semibold">Connected Banks</h3>
          <p className="text-3xl font-bold">0</p>
        </Card>
      </div>
    </div>
  );
}
