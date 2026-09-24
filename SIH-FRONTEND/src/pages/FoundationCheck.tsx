import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle2 } from "lucide-react";

export function FoundationCheck() {
  return (
    <div className="min-h-screen bg-background p-8 md:p-16 flex items-center justify-center">
      <Card className="w-full max-w-xl shadow-lg border-border bg-card">
        <CardHeader className="space-y-3 pb-6">
          <CardTitle className="text-3xl font-medium text-primary tracking-tight">
            Frontend Foundation Ready
          </CardTitle>
          <CardDescription className="text-muted-foreground text-base">
            The core technology stack is initialized and running successfully.
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-8">
          <ul className="space-y-4">
            {[
              "React & Vite setup OK",
              "TypeScript configuration OK",
              "Tailwind CSS v4 custom theme OK",
              "shadcn/ui & Radix primitives OK"
            ].map((item, i) => (
              <li key={i} className="flex items-center gap-3 text-foreground bg-muted/50 p-3 rounded-md border border-border/50">
                <CheckCircle2 className="w-5 h-5 text-secondary flex-shrink-0" />
                <span className="font-medium">{item}</span>
              </li>
            ))}
          </ul>

          <div className="pt-4 border-t border-border flex justify-end">
            <Button className="bg-primary hover:bg-primary/90 text-primary-foreground font-medium px-6 py-2 h-auto shadow-sm transition-all hover:shadow-md">
              Acknowledge
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
