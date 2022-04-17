export interface KNXInfo {
  version: string;
  connected: boolean;
  current_address: string;
}

export interface KNXTelegram {
  destination_address: string;
  source_address: string;
  payload: any;
  direction: string;
  timestamp: Date;
}
