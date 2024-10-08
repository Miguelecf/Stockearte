export interface Store {
  code: string;
  address: string;
  city: string;
  state: string;
  enabled: boolean;
}

export interface Product {
  name: string;
  uniqueCode: string;
  size: string;
  imageUrl: string;
  color: string;
  enabled: boolean;
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}
