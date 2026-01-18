import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPooling2D, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
import os

# --- CONFIGURATION ---
IMG_SIZE = 48
BATCH_SIZE = 64
TRAIN_PATH = 'data/train'
TEST_PATH = 'data/test'

def build_model(input_shape=(48, 48, 1), num_classes=7):
    input_layer = Input(shape=input_shape)

    # ============================================================
    # PART 1: THE CNN ("The Eyes") - Spatial Feature Extraction
    # ============================================================
    # These layers look at the image to find edges, curves, and shapes.
    # They do NOT know what an emotion is yet; they just see patterns.
    
    # CNN Block 1 (Basic Edges)
    x = Conv2D(8, (3, 3), padding='same', use_bias=False)(input_layer)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.2)(x)
    
    # CNN Block 2 (Textures & Shapes)
    x = Conv2D(16, (3, 3), padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.2)(x)

    # CNN Block 3 (Complex Features like Eyes/Mouth)
    x = Conv2D(32, (3, 3), padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.2)(x)
    
    # CNN Block 4 (High-Level Abstract Features)
    x = Conv2D(64, (3, 3), padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Dropout(0.2)(x)

    # ============================================================
    # PART 2: THE ANN ("The Brain") - Classification
    # ============================================================
    # These layers take the "shapes" found by the CNN and decide
    # which emotion category they belong to.
    
    # Connector: Transition from Feature Map to Categories
    x = Conv2D(num_classes, (3, 3), padding='same')(x)
    
    # Flattening: Squashing the 2D grid into a 1D vector
    x = GlobalAveragePooling2D()(x)
    
    # Decision Layer (Softmax):
    # Calculates the % probability for "Happy", "Sad", etc.
    output = Activation('softmax')(x) 
    
    return Model(inputs=input_layer, outputs=output)


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    
    # 1. SETUP DATA PIPELINE
    print("⏳ Setting up data pipeline...")
    
    # Augmentation: Helps the CNN learn to see "tilted" or "zoomed" faces
    train_datagen = ImageDataGenerator(
        rescale=1./255,         
        rotation_range=15,      
        width_shift_range=0.1, 
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    test_datagen = ImageDataGenerator(rescale=1./255)

    # Load images from folders
    train_generator = train_datagen.flow_from_directory(
        TRAIN_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        color_mode='grayscale', 
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )

    validation_generator = test_datagen.flow_from_directory(
        TEST_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    # 2. BUILD & COMPILE
    model = build_model(num_classes=7)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Create models folder
    if not os.path.exists('models'): os.makedirs('models')

    # 3. TRAIN
    # Note: We use Callbacks to stop early if the ANN stops learning
    checkpoint = ModelCheckpoint('models/emotion_model.keras', monitor='val_accuracy', verbose=1, save_best_only=True)
    early_stop = EarlyStopping(patience=8, restore_best_weights=True)
    # Factor 0.2 means "When stuck, slow down the learning by 5x to find the perfect spot"
    reduce_lr = ReduceLROnPlateau(factor=0.2, patience=3, verbose=1, min_lr=0.00001)
    
    print("🚀 Starting Training (CNN + ANN)...")
    
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        epochs=100, 
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // BATCH_SIZE,
        callbacks=[checkpoint, early_stop, reduce_lr]
    )
    
    print("🎉 Training Done! Model saved to models/emotion_model.keras")