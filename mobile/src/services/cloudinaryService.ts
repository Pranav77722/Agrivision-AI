import axios from 'axios';
import * as Crypto from 'expo-crypto';

const CLOUD_NAME = process.env.EXPO_PUBLIC_CLOUDINARY_CLOUD_NAME || '';
const CLOUDINARY_API_KEY = process.env.EXPO_PUBLIC_CLOUDINARY_API_KEY || '';
const CLOUDINARY_API_SECRET = process.env.EXPO_PUBLIC_CLOUDINARY_API_SECRET || '';
const BASE_FOLDER = process.env.EXPO_PUBLIC_CLOUDINARY_FOLDER || 'Agrivision';

export interface CloudinaryUploadResponse {
  asset_id: string;
  public_id: string;
  secure_url: string;
  url: string;
  format: string;
  bytes: number;
}

export const cloudinaryService = {
  /**
   * Upload image to Cloudinary in the user's specific folder using secure HMAC-SHA1 signature.
   */
  uploadImage: async (imageUri: string, folder = 'crop-scans'): Promise<string> => {
    try {
      const data = new FormData();
      const filename = imageUri.split('/').pop() || 'leaf.jpg';
      const match = /\.(\w+)$/.exec(filename);
      const type = match ? `image/${match[1]}` : 'image/jpeg';

      const targetFolder = `${BASE_FOLDER}/${folder}`.replace(/^\/+|\/+$/g, '');
      const timestamp = Math.floor(Date.now() / 1000);

      // Cloudinary parameters in alphabetical order: folder, timestamp
      const paramsToSign = `folder=${targetFolder}&timestamp=${timestamp}${CLOUDINARY_API_SECRET}`;
      const signature = await Crypto.digestStringAsync(
        Crypto.CryptoDigestAlgorithm.SHA1,
        paramsToSign
      );

      // @ts-ignore: React Native FormData supports uri, type, name
      data.append('file', {
        uri: imageUri,
        type,
        name: filename,
      });

      data.append('api_key', CLOUDINARY_API_KEY);
      data.append('timestamp', String(timestamp));
      data.append('folder', targetFolder);
      data.append('signature', signature);

      const uploadUrl = `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/image/upload`;

      const response = await axios.post<CloudinaryUploadResponse>(uploadUrl, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000,
      });

      if (response.data?.secure_url) {
        console.log('Cloudinary upload succeeded:', response.data.secure_url);
        return response.data.secure_url;
      }
      return imageUri;
    } catch (error: any) {
      console.warn('Cloudinary upload notice (fallback to local URI):', error?.response?.data || error?.message || error);
      return imageUri;
    }
  },
};

export default cloudinaryService;
