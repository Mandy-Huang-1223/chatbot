import { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
} from "@mui/material";

export const NewChatroomDialogue = ({
  isNewChatRoomDialogOpen,
  handleNewChatRoomClose,
  handleCreateNewChatRoom,
}: {
  isNewChatRoomDialogOpen: boolean;
  handleNewChatRoomClose: () => void;
  handleCreateNewChatRoom: (name: string) => void;
}) => {
  const [newChatRoomName, setNewChatRoomName] = useState("");
  return (
    <Dialog open={isNewChatRoomDialogOpen} onClose={handleNewChatRoomClose}>
      <DialogTitle>Create New Chat Room</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          id="name"
          label="Chat Room Name"
          type="text"
          fullWidth
          variant="standard"
          value={newChatRoomName}
          onChange={(e) => setNewChatRoomName(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleNewChatRoomClose}>Cancel</Button>
        <Button onClick={() => handleCreateNewChatRoom(newChatRoomName)}>
          Create
        </Button>
      </DialogActions>
    </Dialog>
  );
};
