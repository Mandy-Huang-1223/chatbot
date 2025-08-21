import { ListItem, Box } from "@mui/material";
import { styled } from "@mui/system";

export const StyledMessage = styled(ListItem)(
  ({ sender }: { sender: "user" | "ai" }) => ({
    display: "flex",
    justifyContent: sender === "user" ? "flex-end" : "flex-start",
  })
);

export const MessageBubble = styled(Box)(
  ({ sender }: { sender: "user" | "ai" }) => ({
    backgroundColor: sender === "user" ? "#1976d2" : "#ECE5DD",
    borderRadius: "10px",
    padding: "8px 12px",
    marginBottom: "5px",
    maxWidth: "70%",
    color: sender === "user" ? "#FFFFFF" : "#000000",
  })
);
