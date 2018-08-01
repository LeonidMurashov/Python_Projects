from keras.models import load_model
model = load_model('cats_and_dogs_small_2.h5')

model.summary()

print('Metrics:',model.metrics_names)

from keras.preprocessing.image import ImageDataGenerator
test_datagen = ImageDataGenerator(rescale=1./255)

test_dir = 'D:\\Python\\Keras\\cat_dog_data\\test'

test_generator = test_datagen.flow_from_directory(
                    test_dir,
                    target_size=(150, 150),
                    batch_size=1,
                    class_mode='binary')

print(model.evaluate_generator(test_generator,steps=1000, verbose=True))