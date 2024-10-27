import soap from "soap";
import { resolve } from 'path';

class SoapClient {
    private wsdlUrl: string;
    private client: any;

    constructor(wsdlUrl: string) {
        this.wsdlUrl = wsdlUrl;
    }

    async init() {
        return new Promise((resolve, reject) => {
            soap.createClient(this.wsdlUrl, (err: any, client: any) => {
                if (err) {
                    return reject(err);
                }
                this.client = client;
                resolve(client);
            });
        });
    }

    async createOrder(orderData: any) {
        return new Promise((resolve, reject) => {
            this.client.CreateOrder(orderData, (err: any, result: any) => {
                if (err) {
                    return reject(err);
                }
                resolve(result);
            });
        });
    }

    // Agregar otros métodos SOAP si es necesario
}

export default SoapClient;
