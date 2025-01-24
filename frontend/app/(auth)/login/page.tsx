"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { Banana } from "lucide-react";
import { LoginForm } from "@/components/auth/login-form";
import { useAuth } from "@/contexts/auth-provider";

export default function LoginPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [imageUrl, setImageUrl] = useState("");

  useEffect(() => {
    if (user) {
      router.push("/dashboard");
    }
  }, [user, router]);

  useEffect(() => {
    const randomImageNumber = Math.floor(Math.random() * 9) + 1;
    setImageUrl(`/images/banana-${randomImageNumber}.jpg`);
  }, []);

  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="flex flex-col gap-4 p-6 md:p-10">
        <div className="flex justify-center gap-2 md:justify-start">
          <Link href="/" className="flex items-center gap-2 font-medium">
            <div className="flex p-2 items-center justify-center rounded-md bg-primary text-primary-foreground">
              <Banana size={32} />
            </div>
            <div className="text-3xl font-bold">FLOO</div>
          </Link>
        </div>
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">
            <LoginForm />
          </div>
        </div>
      </div>
      <div className="relative hidden bg-muted lg:block">
        {imageUrl && (
          <Image
            src={imageUrl}
            alt="Login background"
            fill
            className="object-cover dark:brightness-[0.2] dark:grayscale"
            priority
          />
        )}
      </div>
    </div>
  );
}
