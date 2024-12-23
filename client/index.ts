import express, { Request, Response } from "express";
import Client from "./client";
import cors from "cors";
import { RequesterBuilder } from "@grpc/grpc-js";

// Correctly specify the gRPC server address
const client = new Client("localhost:50051"); // Use the port your gRPC server listens on

const app = express();
app.use(express.json());
app.use(cors());

//-----------------------------User--------------------------------------------------
app.post("/create-user", async (req: Request, res: Response) => {
  try {
    const {
      username,
      password,
      firstName,
      lastName,
      enabled,
      isCentral,
      storeId,
    } = req.body;
    const user = await client.createUser(
      username,
      password,
      firstName,
      lastName,
      enabled,
      isCentral,
      storeId
    );
    res.status(201).json(user);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error creating user" });
  }
});

app.post("/login", async (req: Request, res: Response) => {
  const { username, password } = req.body;

  try {
    const loginResponse = await client.loginUser(username, password);

    // Aquí se puede crear un nuevo objeto que contenga el mensaje y la respuesta del login
    const responseWithMessage = {
      message: "Login successful",
      user: loginResponse  // Esto contiene todos los detalles del usuario
    };

    res.status(200).json(responseWithMessage); // Enviamos la respuesta completa
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Login failed" });
  }
});


app.get("/search-user", async (req: Request, res: Response) => {
  console.log(req.query);
  try {
    // Extraemos el parámetro de búsqueda
    const { username } = req.query;

    // Llamamos al método de búsqueda de usuario
    const user = await client.searchUser(username as string);

    if (!user) {
      return res.status(404).json({ message: "User not found" });
    }

    // Devolvemos la información del usuario encontrado
    res.status(200).json({ user });
  } catch (error) {
    console.error("Error en el endpoint:", error);
    res.status(500).json({ message: "Error searching for user" });
  }
});

app.get("/list-users", async (req: Request, res: Response) => {
  try {
    const users = await client.listUsers();
    if (!users || users.length === 0) {
      return res.status(404).json({ message: "No users found" });
    }
    res.status(200).json({ users });
  } catch (error) {
    console.error("Error en el endpoint:", error);
    res.status(500).json({ message: "Error listing users" });
  }
});


app.post("/update-user", async (req: Request, res: Response) => {
  try {
    const { id, username, password, firstName, lastName, enabled, isCentral, storeId } = req.body;

    if (!id) {
      return res.status(400).json({ message: "id is required for updating a user" });
    }

    // Llamar al método updateUser del cliente con el id y otros campos
    const updatedUser = await client.updateUser(
      id,
      username,
      password,
      firstName,
      lastName,
      enabled,
      isCentral,
      storeId
    );

    if (!updatedUser) {
      return res.status(404).json({ message: "User not found" });
    }

    res.status(200).json({ message: "User updated successfully", user: updatedUser });
  } catch (error) {
    console.error("Error updating user:", error);
    res.status(500).json({ message: "Error updating user" });
  }
});

//-----------------------------Store--------------------------------------------------
app.post("/create-store", async (req: Request, res: Response) => {
  try {
    // Extract store details from the request body
    const { code, address, city, state, enabled } = req.body;
    // Call the createStore method from the gRPC client
    const store = await client.createStore(code, address, city, state, enabled);

    // Respond with the created store details
    res.status(201).json(store);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error creating store" });
  }
});

app.post("/disable-store", async (req: Request, res: Response) => {
  try {
    const { code, enabled } = req.body;
    const store = await client.disableStore(code, enabled);
    res.status(200).json(store);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error disabling store" });
  }
});

app.get("/search-store", async (req: Request, res: Response) => {
  try {
    const { code, enabled } = req.query;

    const isEnabled = enabled === "true";

    const stores = await client.searchStore(
      code as string,
      isEnabled
    );

    if (!stores || stores.length === 0) {
      return res.status(404).json({ message: "No stores found" });
    }

    res.status(200).json({ stores });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error searching for stores" });
  }
});

app.post("/assign-store", async (req: Request, res: Response) => {
  const { userId, storeCode } = req.body;

  if (!userId || !storeCode) {
    return res
      .status(400)
      .json({ message: "userId and storeCode are required" });
  }

  try {
    const user = await client.assignStoreToUser(userId, storeCode);

    res.status(200).json({
      message: "Store assigned successfully",
      user: {
        id: user.id,
        username: user.username,
        firstName: user.firstName,
        lastName: user.lastName,
        enabled: user.enabled,
        storeId: user.storeId,
      },
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error assigning store" });
  }
});

app.get("/search-user-by-store", async (req: Request, res: Response) => {
  const { storeCode } = req.query; // Asumiendo que el storeCode se envía como un parámetro de consulta

  if (!storeCode) {
    return res.status(400).json({ message: "storeCode is required" });
  }

  try {
    const response = await client.searchUserByStore(storeCode as string);

    // Verificar si hay usuarios en la respuesta
    if (!response.users || response.users.length === 0) {
      return res
        .status(404)
        .json({ message: "No users found for the given store code" });
    }

    res.status(200).json({
      message: "Users retrieved successfully",
      users: response.users, // Aquí simplemente devolvemos los usuarios tal como vienen
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error retrieving users" });
  }
});

// Agregar el updateStore monstruo del lago ness.

//-----------------------------product--------------------------------------------------
app.post("/create-product", async (req: Request, res: Response) => {
  try {
    const { name, size, imageUrl, color, enabled } = req.body;
    const product = await client.createProduct(
      name,
      size,
      imageUrl,
      color,
      enabled
    );
    res.status(201).json(product);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error creating product" });
  }
});

app.post("/disable-product", async (req: Request, res: Response) => {
  try {
    const { uniqueCode, enabled } = req.body;
    const product = await client.disableProduct(uniqueCode, enabled);
    res.status(200).json(product);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error disabling product" });
  }
});

app.post("/update-product", async (req: Request, res: Response) => {
  try {
    const { name, uniqueCode, size, imageUrl, color, enabled } = req.body;

    // Validar que el código único esté presente (ya que es lo que usualmente se usa para buscar el producto)
    if (!uniqueCode) {
      return res
        .status(400)
        .json({ message: "UniqueCode is required for updating a product" });
    }

    // Llamar al método updateProduct del cliente
    const updatedProduct = await client.updateProduct(
      name,
      uniqueCode,
      size,
      imageUrl,
      color,
      enabled
    );

    if (!updatedProduct) {
      return res.status(404).json({ message: "Product not found" });
    }
    res
      .status(200)
      .json({
        message: "Product updated successfully",
        product: updatedProduct,
      });
  } catch (error) {
    console.error("Error updating product:", error);
    res.status(500).json({ message: "Error updating product" });
  }
});

app.get("/search-product", async (req: Request, res: Response) => {
  console.log(req.query);
  try {
    // Extraemos los posibles parámetros de búsqueda, incluyendo enabled
    const { name, uniqueCode, size, color} = req.query;

    // Convertimos 'enabled' a booleano si está presente en la query
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
    res.status(500).json({ message: "Error searching for products" });
  }
});



//-----------------------------PRODUCT_STORE--------------------------------------------------
app.post("/create-product-store", async (req: Request, res: Response) => {
  try {
    console.log(req.body);
    const { storeCode, productCode, stock, enabled } = req.body;

    // Validación de entrada
    if (
      !storeCode ||
      !productCode ||
      stock === undefined ||
      enabled === undefined
    ) {
      return res.status(400).json({ message: "Missing required fields" });
    }

    // Llamada al cliente gRPC para crear la relación ProductStore
    const productStore = await client.createProductStore(
      storeCode,
      productCode,
      stock,
      enabled
    );
    res.status(201).json(productStore);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error creating ProductStore" });
  }
});

//-----------------------------ORDER--------------------------------------------
app.post("/create-order", async (req: Request, res: Response) => {
  try {
    const { storeId, observations, dispatchOrder, items } = req.body;

    const formattedItems = Array.isArray(items) ? items.map(item => ({
      itemCode: item.itemCode,
      color: item.color,
      size: item.size,
      quantity: item.quantity,
    })) : [];

    const order = await client.createOrder(storeId, observations, dispatchOrder, formattedItems);
    res.status(201).json(order);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error creating order" });
  }
});



const port = 3000;
app.listen(port, () => {
  console.log(`Server started on port ${port}`); // Added back the missing console.log line
});
