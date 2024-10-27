/*import { SoapClient } from ".client/soapclient.ts"; 

const soapClient = new SoapClient();

export async function getOrderDetails(req: any, res: any) {
    try {
        const orderId = req.params.id;
        const orderDetails = await soapClient.getOrderById(orderId);
        res.json(orderDetails);
    } catch (error) {
        res.status(500).send('Error fetching order details');
    }
}
*/