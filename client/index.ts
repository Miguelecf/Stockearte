import express, { Request, Response } from 'express';
import Client from './client';

// Correctly specify the gRPC server address
const client = new Client('localhost:50051'); // Use the port your gRPC server listens on

const app = express();
app.use(express.json());

app.post('/create-user', async (req: Request, res: Response) => {
    try {
        const { username, password, firstName, lastName, enabled, storeId } = req.body;
        const user = await client.createUser(username, password, firstName, lastName, enabled, storeId);
        res.status(201).json(user);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error creating user' });
    }
});

app.post('/login', async (req: Request, res: Response) => { // Fixed async syntax
    try {
        const { username, password } = req.body; // Extract username and password
        const message = await client.loginUser(username, password);
        res.status(200).json({ message }); // Send login success message
    } catch (error) {
        console.error(error);
        res.status(401).json({ message: 'Login failed' }); // Return 401 for login failure
    }
});


app.get('/get-user-by-name/:username', async (req: Request, res: Response) => {
    try {
        const username = req.params.username;
        const user = await client.getUserByUsername(username);
        if (!user) {
            res.status(404).json({ message: 'User not found' });
        } else {
            res.json(user);
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error getting user' });
    }
});

const port = 3000;
app.listen(port, () => {
    console.log(`Server started on port ${port}`);
});
