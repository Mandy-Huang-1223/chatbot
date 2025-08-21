export interface Message {
  id: string;
  text: string | null;
  sender: "user" | "ai";
  image?: string | null;
}
