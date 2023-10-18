import { Button } from "@/components/Button";
import React from "react";

const switchThemeDuration = "duration-200";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-screen gap-5">
      <h1
        className={`font-extrabold text-8xl text-slate-900 dark:text-slate-50 ${switchThemeDuration}`}
      >
        DARK MODE
      </h1>
      <h1>Heading</h1>
      <h2>Text</h2>
      <h3>Subtitle</h3>
      <Button variant="contained" className="hover:bg-red">
        DARK MODE
      </Button>
      <p
        className={`p-2 tracking-wide text-2xl rounded-sm text-slate-900 dark:text-slate-50 ${switchThemeDuration}`}
      >
        With Next.js and TailwindCSS
      </p>
    </div>
  );
}
