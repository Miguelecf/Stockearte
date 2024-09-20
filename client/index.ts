import express, { Request, Response } from 'express';
import Client from './client';
import { RequesterBuilder } from '@grpc/grpc-js';

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

app.post('/create-store', async (req: Request, res: Response) => {
    try {
        // Extract store details from the request body
        const { code, address, city, state, enabled } = req.body;
        // Call the createStore method from the gRPC client
        const store = await client.createStore(code, address, city, state, enabled);

        // Respond with the created store details
        res.status(201).json(store);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error creating store' });
    }
});

app.post('/disable-store', async (req: Request, res: Response) => {
    try {
        const { code, enabled } = req.body;
        const store = await client.disableStore(code, enabled);
        res.status(200).json(store);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error disabling store' });
    }
});

//-----------------------------product--------------------------------------------------
app.post('/create-product', async (req: Request, res: Response) => {

    try {
        const { name, unique_code, size, image_url, color, enabled } = req.body;
        const product = await client.createProduct( name, unique_code, size, image_url, color, enabled);
        res.status(201).json(product);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error creating product' });
    }
});

app.post('/disable-product', async (req: Request, res: Response) => {
    try {
        const { unique_code, enabled } = req.body;
        const product = await client.disableProduct(unique_code, enabled);
        res.status(200).json(product);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error disabling product' });
    }
});

app.post('/update-product', async (req: Request, res: Response) => {
    try {
        const { name, unique_code, size, image_url, color, enabled } = req.body;
        const product = await client.updateProduct( name, unique_code, size, image_url, color, enabled);
        res.status(201).json(product);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error creating product' });
    }
});

app.post('/search-product', async (req: Request, res: Response) => {
    console.log(req.body)
    try {
        const { name,unique_code,  size, color } = req.body;
        const products = await client.searchProduct(name,unique_code,  size, color);
        res.status(200).json(products); // Devolver la lista de productos encontrados
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error searching for products' });
    }
});


const port = 3000;
app.listen(port, () => {
    console.log(`Server started on port ${port}`); // Added back the missing console.log line
});