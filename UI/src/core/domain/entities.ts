export interface Store {
  code: string;
  address: string;
  city: string;
  state: string;
  enabled: boolean;
}

export interface Product {
  id: string;
  name: string;
  price: number;
  stock: number;
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}
