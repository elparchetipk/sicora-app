// Imagen en Base64 para usuario por defecto
// El formato es un pequeño PNG de 100x100 con el color verde SENA
export const DEFAULT_PROFILE_IMAGE_BASE64 =
  'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAAD4ElEQVR4nO3dW2/TQBDG8TFCgHgAJO5XQNzyUJC49REQdzgUCQmJj8RX4AZCXCWgRRzHcbKbtWd3Z9f/n+RIrdIm45+P13a8G8YAAAAAAAAAAAAAAAAAAAAAAIC9HJrhJ2Y4lc6h9SbjnRm+muHHmT9/N8NHMzyTzqm1JuPADJc2rss1xJF0bq0SGe9tRNtYI86kcyszGR/VYZihy2S8LfH3aTIZH5xjbIbLkt+nqSLjvXMMfZgqMt47x7gqncOqTMZ75xjnpXNYlcl4L5TE8qs+k/FeKInTK+kcVqWUxNXqOZPx3rkk4qqUQt6PcwzKsDqlEGdZlFI2oQzXpOQY8yJtMt5L5bCJq1JOtyjDypRC/NOuNTt9JlGGlTmTs4R00Wwy3kvlsInfKQf0jdlkvJfKYRNXhk6fSZRhZU4ZrknZU5Px3jkGZVidUsbDOfvxgzX74SiPtX9JVzYZv53792bNfniTY+3fpPPwyphhr+kXAe38o9L5eGXN0G36vVw7Pyudj1cKYYxRCIUwxiiEQhhjFEIhjLEtC/lugzqTzskrZdi2QR3in6Xz8koBF99tk/HXDOel8/JKAecuOJfjqnReXinAet9iP0vn5ZUCkrw3GW9K5+WVAoaGQnJSwPA3hWSjgOEvhWSlgKFLoVduFACFOFMAhTBlUQhTFtNVbgpgysosBZibIQ6bcJebAigkswQ3UUi7sC4rNwVQSGYKYMrKjHVZmTFlZaaEC1/tcnr80Ax3zHA70c9fJucH6Zy8UgKl+EYhuVGKb83+C01K8a3ZhaAU3yjFNQrxjVJ8oxTXKMQ3SvGNUlyjEN8oxTdKcY1CfKMU3yjFNQppH1NWw7BDbDim1obhfUjDsB+rYdiR2DDs6WsY9sU2DDs7G4advQ3D3uuG4YBCw3BEp2E44Nkwa1w+iXkBB6UbZo3Lx5aTGGUb1mBJHNowHLptmKgpyzAsImprMQyLidpaDMOCxrYWw7CouW3FMCzyb1sxDC+WaFsxDC8/als1DO+Qadt/WNvwLr+2FcPwTtG2FcPwbvu2FcPwgZC2FcPwoaK2VcPwwaW2/x8Se2P44OC2gu6o313slfjnuDt8JGCMYRjG0T3jcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDicFOdhrH0qNGTPEexoTwXvJsfYDJdi37PJMf6Z4YH0hdIMnj5bP0O8kL5ImsFTZ8sXDjPcNMOJ9EXTitjb39Jvy7+Y4ZH0BdOK2JvZYiN8E76Z4Vj6omnNZHwJ5fAm7L35lGEF1wzPzfDVDL+kb/haiHmHC85JZnhhhtfSN38txDwvwwupc+mLoBZiHseL+BP+QgxXfxgLWwAAAABJRU5ErkJggg==';

// Función para obtener la imagen por defecto
export const getDefaultProfileImage = () => {
  return { uri: DEFAULT_PROFILE_IMAGE_BASE64 };
};

/**
 * Función para validar si una URL de imagen es válida
 * @param {string} url - URL a validar
 * @returns {boolean} - true si parece una URL válida
 */
export const isValidImageUrl = (url) => {
  if (!url) return false;

  // Verificación básica para URL válida
  return url.startsWith('http') || url.startsWith('data:image') || url.startsWith('file:');
};
