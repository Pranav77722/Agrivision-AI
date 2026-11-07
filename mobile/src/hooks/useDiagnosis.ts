import { useDiagnosisStore } from '../store/diagnosisStore';

export const useDiagnosis = () => {
  const currentDiagnosis = useDiagnosisStore((s) => s.currentDiagnosis);
  const history = useDiagnosisStore((s) => s.history);
  const selectedCrop = useDiagnosisStore((s) => s.selectedCrop);
  const capturedImageUri = useDiagnosisStore((s) => s.capturedImageUri);
  const isLoading = useDiagnosisStore((s) => s.isLoading);
  const error = useDiagnosisStore((s) => s.error);
  const setSelectedCrop = useDiagnosisStore((s) => s.setSelectedCrop);
  const setCapturedImageUri = useDiagnosisStore((s) => s.setCapturedImageUri);
  const setCurrentDiagnosis = useDiagnosisStore((s) => s.setCurrentDiagnosis);
  const addDiagnosis = useDiagnosisStore((s) => s.addDiagnosis);
  const removeDiagnosis = useDiagnosisStore((s) => s.removeDiagnosis);

  return {
    currentDiagnosis,
    history,
    selectedCrop,
    capturedImageUri,
    isLoading,
    error,
    setSelectedCrop,
    setCapturedImageUri,
    setCurrentDiagnosis,
    addDiagnosis,
    removeDiagnosis,
  };
};

export default useDiagnosis;
