"use client";

import { useEffect, useState } from "react";
import { Bank } from "@/types/bank";
import { getBanks, createBank, updateBank, deleteBank } from "@/services/bank";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { Pencil, Trash2, Plus } from "lucide-react";

export default function BanksPage() {
  const [banks, setBanks] = useState<Bank[]>([]);
  const [isLoadingBanks, setIsLoadingBanks] = useState(true);
  const [selectedBank, setSelectedBank] = useState<Bank | null>(null);
  const [newBankName, setNewBankName] = useState("");
  const [newBankColor, setNewBankColor] = useState("#000000");
  const [newBankBalance, setNewBankBalance] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const { toast } = useToast();

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const fetchBanks = async () => {
    setIsLoadingBanks(true);
    try {
      const data = await getBanks();
      setBanks(data);
    } catch (error) {
      toast({
        title: "Error",
        description:
          error instanceof Error ? error.message : "Failed to fetch banks",
        variant: "destructive",
      });
    } finally {
      setIsLoadingBanks(false);
    }
  };

  useEffect(() => {
    fetchBanks();
  }, []);

  const handleCreateBank = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    try {
      await createBank(newBankName, newBankColor, newBankBalance);
      await fetchBanks();
      setNewBankName("");
      setNewBankColor("#000000");
      setNewBankBalance(0);
      setIsCreateOpen(false);
      toast({
        title: "Success",
        description: "Bank created successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description:
          error instanceof Error ? error.message : "Failed to create bank",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleEditBank = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!selectedBank) return;
    setIsLoading(true);
    try {
      await updateBank(
        selectedBank.id,
        newBankName,
        newBankColor,
        newBankBalance
      );
      await fetchBanks();
      setSelectedBank(null);
      setNewBankName("");
      setNewBankColor("#000000");
      setNewBankBalance(0);
      setIsEditOpen(false);
      toast({
        title: "Success",
        description: "Bank updated successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description:
          error instanceof Error ? error.message : "Failed to update bank",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteBank = async () => {
    if (!selectedBank) return;
    setIsLoading(true);
    setDeleteError(null);
    try {
      await deleteBank(selectedBank.id);
      await fetchBanks();
      setSelectedBank(null);
      setIsDeleteOpen(false);
      toast({
        title: "Success",
        description: "Bank deleted successfully",
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Failed to delete bank";
      setDeleteError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const openEditDialog = (bank: Bank) => {
    setSelectedBank(bank);
    setNewBankName(bank.name);
    setNewBankColor(bank.color);
    setNewBankBalance(bank.start_balance);
    setIsEditOpen(true);
  };

  const openDeleteDialog = (bank: Bank) => {
    setSelectedBank(bank);
    setDeleteError(null);
    setIsDeleteOpen(true);
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Banks</h1>
        <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
          <DialogTrigger asChild>
            <Button size="icon">
              <Plus className="h-4 w-4" />
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New Bank</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleCreateBank} className="space-y-4">
              <div>
                <label
                  htmlFor="bankName"
                  className="block text-sm font-medium mb-1"
                >
                  Bank Name
                </label>
                <Input
                  id="bankName"
                  placeholder="Bank name"
                  value={newBankName}
                  onChange={(e) => setNewBankName(e.target.value)}
                  required
                />
              </div>
              <div>
                <label
                  htmlFor="bankColor"
                  className="block text-sm font-medium mb-1"
                >
                  Color
                </label>
                <Input
                  id="bankColor"
                  type="color"
                  value={newBankColor}
                  onChange={(e) => setNewBankColor(e.target.value)}
                  required
                />
              </div>
              <div>
                <label
                  htmlFor="bankBalance"
                  className="block text-sm font-medium mb-1"
                >
                  Start Balance
                </label>
                <Input
                  id="bankBalance"
                  type="number"
                  min="0"
                  placeholder="Initial balance"
                  value={newBankBalance}
                  onChange={(e) => setNewBankBalance(Number(e.target.value))}
                  required
                />
              </div>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Creating..." : "Create Bank"}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Start Balance</TableHead>
              <TableHead>End Balance</TableHead>
              <TableHead className="w-[100px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoadingBanks ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center">
                  Loading banks...
                </TableCell>
              </TableRow>
            ) : banks.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center">
                  No banks found
                </TableCell>
              </TableRow>
            ) : (
              banks.map((bank) => (
                <TableRow key={bank.id}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div
                        className="w-4 h-4 rounded-full"
                        style={{ backgroundColor: bank.color }}
                      />
                      {bank.name}
                    </div>
                  </TableCell>
                  <TableCell>{formatCurrency(bank.start_balance)}</TableCell>
                  <TableCell>{formatCurrency(bank.end_balance)}</TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => openEditDialog(bank)}
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="icon"
                        onClick={() => openDeleteDialog(bank)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </Card>

      {/* Edit Dialog */}
      <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Bank</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleEditBank} className="space-y-4">
            <div>
              <label
                htmlFor="editBankName"
                className="block text-sm font-medium mb-1"
              >
                Bank Name
              </label>
              <Input
                id="editBankName"
                placeholder="Bank name"
                value={newBankName}
                onChange={(e) => setNewBankName(e.target.value)}
                required
              />
            </div>
            <div>
              <label
                htmlFor="editBankColor"
                className="block text-sm font-medium mb-1"
              >
                Color
              </label>
              <Input
                id="editBankColor"
                type="color"
                value={newBankColor}
                onChange={(e) => setNewBankColor(e.target.value)}
                required
              />
            </div>
            <div>
              <label
                htmlFor="editBankBalance"
                className="block text-sm font-medium mb-1"
              >
                Start Balance
              </label>
              <Input
                id="editBankBalance"
                type="number"
                min="0"
                placeholder="Initial balance"
                value={newBankBalance}
                onChange={(e) => setNewBankBalance(Number(e.target.value))}
                required
              />
            </div>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Saving..." : "Save Changes"}
            </Button>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={isDeleteOpen} onOpenChange={setIsDeleteOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="text-xl">Delete Bank</DialogTitle>
            <div className="mt-4 space-y-2">
              <DialogDescription asChild>
                <div>
                  Are you sure you want to delete{" "}
                  <span className="font-medium">{selectedBank?.name}</span>?
                  <br />
                  This action cannot be undone.
                </div>
              </DialogDescription>
              {isLoading && (
                <div className="text-sm text-muted-foreground">
                  Deleting bank...
                </div>
              )}
              {deleteError && (
                <div className="text-sm text-destructive">
                  {deleteError.includes("transactions exist")
                    ? "This bank cannot be deleted because it has transactions linked to it. Please delete all associated transactions first."
                    : deleteError}
                </div>
              )}
            </div>
          </DialogHeader>
          <div className="flex justify-end gap-2">
            <Button
              variant="outline"
              onClick={() => setIsDeleteOpen(false)}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDeleteBank}
              disabled={isLoading}
            >
              {isLoading ? "Deleting..." : "Delete"}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
