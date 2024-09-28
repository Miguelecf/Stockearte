import express, { Request, Response } from 'express';
import Client from './client';
import { RequesterBuilder } from '@grpc/grpc-js';

// Correctly specify the gRPC server address
const client = new Client('localhost:50051'); // Use the port your gRPC server listens on

const app = express();
app.use(express.json());

//-----------------------------User--------------------------------------------------
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

app.get('/search-user', async (req: Request, res: Response) => {
    console.log(req.query);
    try {
        // Extraemos el parámetro de búsqueda
        const { username } = req.query;

        // Llamamos al método de búsqueda de usuario
        const user = await client.searchUser(username as string);

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        // Devolvemos la información del usuario encontrado
        res.status(200).json({ user });
    } catch (error) {
        console.error('Error en el endpoint:', error);
        res.status(500).json({ message: 'Error searching for user' });
    }
});

app.post('/update-user', async (req: Request, res: Response) => {
    console.log("Index.ts -> Request body", req.body)
    try {
        const {
            username,
            password,
            firstName,
            lastName,
            enabled } = req.body;

        if (!username) {
            return res.status(400).json({ message: 'username is required for updating a user' });
        }

        // Llamar al método updateUser del cliente
        const updatedUser = await client.updateUser(username, password, firstName, lastName, enabled);

        if (!updatedUser) {
            return res.status(404).json({ message: 'User not found' });
        }

        res.status(200).json({ message: 'User updated successfully', user: updatedUser });
    } catch (error) {
        console.error('Error updating user:', error);
        res.status(500).json({ message: 'Error updating user' });
    }
});

//-----------------------------Store--------------------------------------------------
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

app.get('/search-store', async (req: Request, res: Response) => {
    try {
        const { code, enabled } = req.query;

        // Convertimos 'enabled' a booleano correctamente
        const isEnabled = enabled === 'true'; // Solo será true si el valor de enabled es exactamente 'true'

        const stores = await client.searchStore(
            code as string,
            isEnabled // Pasamos el valor booleano real
        );

        if (!stores || stores.length === 0) {
            return res.status(404).json({ message: 'No stores found' });
        }

        res.status(200).json({ stores });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error searching for stores' });
    }
});


//-----------------------------product--------------------------------------------------
app.post('/create-product', async (req: Request, res: Response) => {
    try {
        const { name,
            size,
            imageUrl,
            color,
            enabled } = req.body;
        const product = await client.createProduct(name, size, imageUrl, color, enabled);
        res.status(201).json(product);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error creating product' });
    }
});

app.post('/disable-product', async (req: Request, res: Response) => {
    try {
        const {
            uniqueCode,
            enabled } = req.body;
        const product = await client.disableProduct(uniqueCode, enabled);
        res.status(200).json(product);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error disabling product' });
    }
});

app.post('/update-product', async (req: Request, res: Response) => {
    try {
        const {
            name,
            uniqueCode,
            size,
            imageUrl,
            color,
            enabled } = req.body;

        // Validar que el código único esté presente (ya que es lo que usualmente se usa para buscar el producto)
        if (!uniqueCode) {
            return res.status(400).json({ message: 'UniqueCode is required for updating a product' });
        }

        // Llamar al método updateProduct del cliente
        const updatedProduct = await client.updateProduct(name, uniqueCode, size, imageUrl, color, enabled);

        if (!updatedProduct) {
            return res.status(404).json({ message: 'Product not found' });
        }
        res.status(200).json({ message: 'Product updated successfully', product: updatedProduct });
    } catch (error) {
        console.error('Error updating product:', error)
        res.status(500).json({ message: 'Error updating product' });
    }
});


app.get('/search-product', async (req: Request, res: Response) => {
    console.log(req.query);
    try {
        // Extraemos los posibles parámetros de búsqueda
        const { name, uniqueCode, size, color } = req.query;

        // Llamamos a la función searchProduct pasando los valores extraídos de la query
        const products = await client.searchProduct(
            name as string,
            uniqueCode as string,
            size as string,
            color as string
        );

        // Devolvemos la lista de productos encontrados
        res.status(200).json(products);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error searching for products' });
    }
});




const port = 3000;
app.listen(port, () => {
    console.log(`Server started on port ${port}`); // Added back the missing console.log line
});