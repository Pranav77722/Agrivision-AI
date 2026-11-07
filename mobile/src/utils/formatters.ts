import { format, parseISO } from 'date-fns';

export const formatDate = (dateString: string, dateFormat = 'dd MMM yyyy, hh:mm a'): string => {
  try {
    const parsed = typeof dateString === 'string' ? parseISO(dateString) : dateString;
    return format(parsed, dateFormat);
  } catch {
    return dateString;
  }
};

export const formatConfidence = (score: number): string => {
  return `${Math.round(score * 10) / 10}%`;
};

export const formatCurrencyInr = (amount: number): string => {
  return `₹${amount.toLocaleString('en-IN')}`;
};

export const formatArea = (acres: number): string => {
  return `${acres} Acre${acres === 1 ? '' : 's'}`;
};
