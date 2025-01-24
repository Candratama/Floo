import { RegisterForm } from "@/components/auth/register-form";
import Image from "next/image";
import Link from "next/link";

export default function RegisterPage() {
  return (
    <div className="container grid h-screen w-screen flex-col items-center justify-center lg:max-w-none lg:grid-cols-2 lg:px-0">
      <Link
        href="/login"
        className="absolute left-4 top-4 flex items-center text-sm font-medium md:left-8 md:top-8"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="mr-2 h-4 w-4"
        >
          <path d="m15 18-6-6 6-6" />
        </svg>
        Back to login
      </Link>

      <div className="hidden h-full bg-muted lg:block">
        <Image
          src="/images/banana-9.jpg"
          alt="Authentication"
          width={1920}
          height={1080}
          className="h-full w-full object-cover dark:brightness-50"
        />
      </div>

      <div className="lg:p-8">
        <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
          <RegisterForm />
        </div>
      </div>
    </div>
  );
}
