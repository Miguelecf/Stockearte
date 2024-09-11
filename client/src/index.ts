import express from "express";
import cors from "cors";
import client from "./client";

const app = express();
app.use(express.json());
app.use(cors({
  origin: '*',
}));

app.post("/login", async (req, res) => {
  const { user, password } = req.body;
  console.log(user, password);
  try {
    const message = await client.login(user, password);
    res.json({ message });
  } catch (error) {
    if (error instanceof Error) {
      res.status(500).json({ error: error.message });
    } else {
      res.status(500).json({ error: "Unknown error occurred" });
    }
  }
});

// Inicia el servidor en el puerto 3000
app.listen(3000, () => {
  console.log("API server running on port 3000");
});
