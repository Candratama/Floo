"use client";

import { useEffect, useState } from "react";
import { Category } from "@/types/category";
import {
  getCategories,
  createCategory,
  updateCategory,
  deleteCategory,
} from "@/services/category";
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

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoadingCategories, setIsLoadingCategories] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(
    null
  );
  const [newCategoryName, setNewCategoryName] = useState("");
  const [newIsIncome, setNewIsIncome] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const { toast } = useToast();

  const fetchCategories = async () => {
    setIsLoadingCategories(true);
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (error) {
      toast({
        title: "Error",
        description:
          error instanceof Error ? error.message : "Failed to fetch categories",
        variant: "destructive",
      });
    } finally {
      setIsLoadingCategories(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleCreateCategory = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    try {
      await createCategory(newCategoryName, newIsIncome);
      await fetchCategories();
      setNewCategoryName("");
      setNewIsIncome(false);
      setIsCreateOpen(false);
      toast({
        title: "Success",
        description: "Category created successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description:
          error instanceof Error ? error.message : "Failed to create category",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleEditCategory = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!selectedCategory) return;
    setIsLoading(true);
    try {
      await updateCategory(selectedCategory.id, newCategoryName, newIsIncome);
      await fetchCategories();
      setSelectedCategory(null);
      setNewCategoryName("");
      setNewIsIncome(false);
      setIsEditOpen(false);
      toast({
        title: "Success",
        description: "Category updated successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description:
          error instanceof Error ? error.message : "Failed to update category",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteCategory = async () => {
    if (!selectedCategory) return;
    setIsLoading(true);
    setDeleteError(null);
    try {
      await deleteCategory(selectedCategory.id);
      await fetchCategories();
      setSelectedCategory(null);
      setIsDeleteOpen(false);
      toast({
        title: "Success",
        description: "Category deleted successfully",
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Failed to delete category";
      setDeleteError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const openEditDialog = (category: Category) => {
    setSelectedCategory(category);
    setNewCategoryName(category.name);
    setNewIsIncome(category.is_income);
    setIsEditOpen(true);
  };

  const openDeleteDialog = (category: Category) => {
    setSelectedCategory(category);
    setDeleteError(null);
    setIsDeleteOpen(true);
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Categories</h1>
        <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
          <DialogTrigger asChild>
            <Button size="icon">
              <Plus className="h-4 w-4" />
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New Category</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleCreateCategory} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Category Name
                </label>
                <Input
                  placeholder="Category name"
                  value={newCategoryName}
                  onChange={(e) => setNewCategoryName(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium mb-1">
                  Category Type
                </label>
                <div className="flex space-x-4">
                  <div className="flex items-center space-x-2">
                    <input
                      type="radio"
                      id="categoryTypeExpense"
                      name="categoryType"
                      className="h-4 w-4 appearance-none rounded-full border border-yellow-500 checked:bg-yellow-500 checked:border-yellow-500 focus:ring-yellow-500 focus:ring-2 focus:ring-offset-2"
                      checked={!newIsIncome}
                      onChange={() => setNewIsIncome(false)}
                    />
                    <label htmlFor="categoryTypeExpense" className="text-sm">
                      Expense
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input
                      type="radio"
                      id="categoryTypeIncome"
                      name="categoryType"
                      className="h-4 w-4 appearance-none rounded-full border border-yellow-500 checked:bg-yellow-500 checked:border-yellow-500 focus:ring-yellow-500 focus:ring-2 focus:ring-offset-2"
                      checked={newIsIncome}
                      onChange={() => setNewIsIncome(true)}
                    />
                    <label htmlFor="categoryTypeIncome" className="text-sm">
                      Income
                    </label>
                  </div>
                </div>
              </div>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Creating..." : "Create Category"}
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
              <TableHead>Type</TableHead>
              <TableHead className="w-[100px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoadingCategories ? (
              <TableRow>
                <TableCell colSpan={3} className="text-center">
                  Loading categories...
                </TableCell>
              </TableRow>
            ) : categories.length === 0 ? (
              <TableRow>
                <TableCell colSpan={3} className="text-center">
                  No categories found
                </TableCell>
              </TableRow>
            ) : (
              [...categories]
                .sort((a, b) => {
                  // Sort by type first (expense before income)
                  if (a.is_income !== b.is_income) {
                    return a.is_income ? 1 : -1;
                  }
                  // Then sort alphabetically by name
                  return a.name.localeCompare(b.name);
                })
                .map((category) => (
                  <TableRow key={category.id}>
                    <TableCell>{category.name}</TableCell>
                    <TableCell>
                      <span
                        className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${
                          category.is_income
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {category.is_income ? "Income" : "Expense"}
                      </span>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={() => openEditDialog(category)}
                        >
                          <Pencil className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="destructive"
                          size="icon"
                          onClick={() => openDeleteDialog(category)}
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
            <DialogTitle>Edit Category</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleEditCategory} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                Category Name
              </label>
              <Input
                placeholder="Category name"
                value={newCategoryName}
                onChange={(e) => setNewCategoryName(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <label className="block text-sm font-medium mb-1">
                Category Type
              </label>
              <div className="flex space-x-4">
                <div className="flex items-center space-x-2">
                  <input
                    type="radio"
                    id="editCategoryTypeExpense"
                    name="editCategoryType"
                    className="h-4 w-4 appearance-none rounded-full border border-yellow-500 checked:bg-yellow-500 checked:border-yellow-500 focus:ring-yellow-500 focus:ring-2 focus:ring-offset-2"
                    checked={!newIsIncome}
                    onChange={() => setNewIsIncome(false)}
                  />
                  <label htmlFor="editCategoryTypeExpense" className="text-sm">
                    Expense
                  </label>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="radio"
                    id="editCategoryTypeIncome"
                    name="editCategoryType"
                    className="h-4 w-4 accent-yellow-500"
                    checked={newIsIncome}
                    onChange={() => setNewIsIncome(true)}
                  />
                  <label htmlFor="editCategoryTypeIncome" className="text-sm">
                    Income
                  </label>
                </div>
              </div>
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
            <DialogTitle className="text-xl">Delete Category</DialogTitle>
            <div className="mt-4 space-y-2">
              <DialogDescription asChild>
                <div>
                  Are you sure you want to delete{" "}
                  <span className="font-medium">{selectedCategory?.name}</span>?
                  <br />
                  This action cannot be undone.
                </div>
              </DialogDescription>
              {isLoading && (
                <div className="text-sm text-muted-foreground">
                  Deleting category...
                </div>
              )}
              {deleteError && (
                <div className="text-sm text-destructive">
                  {deleteError.includes("transactions exist")
                    ? "This category cannot be deleted because it has transactions linked to it. Please delete all associated transactions first."
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
              onClick={handleDeleteCategory}
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
