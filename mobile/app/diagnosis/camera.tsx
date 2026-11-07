import React, { useState, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Button } from '../../src/components/ui/Button';
import { useDiagnosisStore } from '../../src/store/diagnosisStore';
import { pickImageFromGallery } from '../../src/utils/imageUtils';

export default function CameraScreen() {
  const { t } = useTranslation(['diagnosis', 'common']);
  const router = useRouter();
  const [permission, requestPermission] = useCameraPermissions();
  const [facing, setFacing] = useState<'back' | 'front'>('back');
  const [flash, setFlash] = useState<'off' | 'on'>('off');
  const cameraRef = useRef<any>(null);
  const setCapturedImageUri = useDiagnosisStore((s) => s.setCapturedImageUri);

  if (!permission) {
    return <View style={styles.blackBackground} />;
  }

  if (!permission.granted) {
    return (
      <SafeArea style={styles.permissionContainer}>
        <View style={styles.permissionContent}>
          <Ionicons name="camera-outline" size={64} color="#16A34A" />
          <Text style={styles.permissionTitle}>{t('diagnosis:cameraPermission')}</Text>
          <Button
            size="lg"
            title={t('diagnosis:grantPermission')}
            variant="primary"
            onPress={requestPermission}
          />
        </View>
      </SafeArea>
    );
  }

  const handleCapture = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync({
          quality: 0.65,
          skipProcessing: false,
        });
        if (photo?.uri) {
          setCapturedImageUri(photo.uri);
          router.push('/diagnosis/preview' as any);
        }
      } catch (err) {
        console.error('Camera capture error:', err);
      }
    }
  };

  const handleGallery = async () => {
    const result = await pickImageFromGallery();
    if (result) {
      setCapturedImageUri(result.uri);
      router.push('/diagnosis/preview' as any);
    }
  };

  const toggleFlash = () => {
    setFlash((prev) => (prev === 'off' ? 'on' : 'off'));
  };

  const toggleCameraFacing = () => {
    setFacing((prev) => (prev === 'back' ? 'front' : 'back'));
  };

  return (
    <View style={styles.container}>
      <CameraView
        ref={cameraRef}
        enableTorch={flash === 'on'}
        facing={facing}
        style={StyleSheet.absoluteFill}
      />

      {/* Top Controls Overlay */}
      <View style={styles.topBar}>
        <TouchableOpacity
          accessibilityRole="button"
          hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          style={styles.iconButton}
          onPress={() => router.back()}
        >
          <Ionicons name="close" size={26} color="#FFFFFF" />
        </TouchableOpacity>

        <View style={styles.topRightControls}>
          <TouchableOpacity
            accessibilityRole="button"
            style={styles.iconButton}
            onPress={toggleFlash}
          >
            <Ionicons
              name={flash === 'on' ? 'flash' : 'flash-off'}
              size={22}
              color={flash === 'on' ? '#F59E0B' : '#FFFFFF'}
            />
          </TouchableOpacity>

          <TouchableOpacity
            accessibilityRole="button"
            style={styles.iconButton}
            onPress={toggleCameraFacing}
          >
            <Ionicons name="camera-reverse-outline" size={24} color="#FFFFFF" />
          </TouchableOpacity>
        </View>
      </View>

      {/* Center Target Box / Leaf Guide Overlay */}
      <View style={styles.centerOverlay}>
        <View style={styles.guideFrame}>
          <View style={[styles.corner, styles.topLeft]} />
          <View style={[styles.corner, styles.topRight]} />
          <View style={[styles.corner, styles.bottomLeft]} />
          <View style={[styles.corner, styles.bottomRight]} />
        </View>
        <Text style={styles.guideText}>{t('diagnosis:positionLeafGuide')}</Text>
      </View>

      {/* Bottom Shutter & Controls Bar */}
      <View style={styles.bottomBar}>
        <TouchableOpacity
          accessibilityRole="button"
          style={styles.sideButton}
          onPress={handleGallery}
        >
          <Ionicons name="images" size={26} color="#FFFFFF" />
        </TouchableOpacity>

        <TouchableOpacity
          accessibilityRole="button"
          activeOpacity={0.8}
          style={styles.shutterOuter}
          onPress={handleCapture}
        >
          <View style={styles.shutterInner} />
        </TouchableOpacity>

        <View style={styles.sidePlaceholder} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
  blackBackground: {
    flex: 1,
    backgroundColor: '#000000',
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  permissionContent: {
    alignItems: 'center',
    gap: 16,
    maxWidth: 300,
  },
  permissionTitle: {
    fontSize: 16,
    fontWeight: '700',
    textAlign: 'center',
    lineHeight: 22,
  },
  topBar: {
    position: 'absolute',
    top: 50,
    left: 20,
    right: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    zIndex: 10,
  },
  topRightControls: {
    flexDirection: 'row',
    gap: 12,
  },
  iconButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(0, 0, 0, 0.45)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  centerOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  guideFrame: {
    width: 280,
    height: 280,
    position: 'relative',
    backgroundColor: 'transparent',
  },
  corner: {
    position: 'absolute',
    width: 32,
    height: 32,
    borderColor: '#22C55E',
  },
  topLeft: {
    top: 0,
    left: 0,
    borderTopWidth: 4,
    borderLeftWidth: 4,
    borderTopLeftRadius: 16,
  },
  topRight: {
    top: 0,
    right: 0,
    borderTopWidth: 4,
    borderRightWidth: 4,
    borderTopRightRadius: 16,
  },
  bottomLeft: {
    bottom: 0,
    left: 0,
    borderBottomWidth: 4,
    borderLeftWidth: 4,
    borderBottomLeftRadius: 16,
  },
  bottomRight: {
    bottom: 0,
    right: 0,
    borderBottomWidth: 4,
    borderRightWidth: 4,
    borderBottomRightRadius: 16,
  },
  guideText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
    marginTop: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.55)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  bottomBar: {
    position: 'absolute',
    bottom: 40,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  sideButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  sidePlaceholder: {
    width: 48,
    height: 48,
  },
  shutterOuter: {
    width: 76,
    height: 76,
    borderRadius: 38,
    borderWidth: 4,
    borderColor: '#FFFFFF',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  shutterInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
  },
});
