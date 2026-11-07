import { z } from 'zod';

export const loginSchema = z.object({
  phoneOrEmail: z
    .string()
    .min(3, { message: 'Please enter valid phone or email' })
    .max(100),
  password: z
    .string()
    .min(6, { message: 'Password must be at least 6 characters' }),
});

export type LoginFormData = z.infer<typeof loginSchema>;

export const registerSchema = z
  .object({
    fullName: z
      .string()
      .min(2, { message: 'Name must be at least 2 characters' })
      .max(60),
    phoneNumber: z
      .string()
      .min(10, { message: 'Mobile number must be at least 10 digits' })
      .max(15),
    email: z.string().email({ message: 'Invalid email address' }).optional().or(z.literal('')),
    password: z
      .string()
      .min(6, { message: 'Password must be at least 6 characters' }),
    confirmPassword: z.string(),
    village: z
      .string()
      .min(2, { message: 'Village name is required' }),
    district: z
      .string()
      .min(2, { message: 'District is required' }),
    state: z
      .string()
      .min(2, { message: 'State is required' }),
    totalAcres: z.number().min(0.1).max(1000).optional(),
    primaryCrops: z.array(z.string()).optional(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

export type RegisterFormData = z.infer<typeof registerSchema>;

export const yieldPredictionSchema = z.object({
  crop: z.enum(['tomato', 'rice', 'wheat', 'cotton', 'potato', 'maize', 'soybean', 'sugarcane']),
  district: z.string().min(2, { message: 'District name is required' }),
  areaAcres: z.number().min(0.1, { message: 'Minimum area is 0.1 acre' }).max(1000),
  soilType: z.enum(['black', 'alluvial', 'red', 'sandy', 'clay']),
  season: z.enum(['kharif', 'rabi', 'zaid']),
  irrigation: z.enum(['drip', 'sprinkler', 'canal', 'rainfed']),
});

export type YieldPredictionFormData = z.infer<typeof yieldPredictionSchema>;
