import unittest
from unittest.mock import patch
from src.faq import get_faq_suggestions
import pdb

class TestFaqSuggestions(unittest.TestCase):

    def test_get_faq_suggestions_internet(self):
        input_text = "Tengo problemas con internet, no sé qué hacer."
        response = get_faq_suggestions(input_text)
        #pdb.set_trace()
        suggestions = response.split("\n")
        self.assertEqual(len(suggestions), 5)
        self.assertTrue(all(suggestion.startswith(str(i+1)) for i, suggestion in enumerate(suggestions)))
    
    def test_get_faq_suggestions_email(self):
        input_text = "No puedo enviar correos desde mi email."
        response = get_faq_suggestions(input_text)
        suggestions = response.split("\n")
        self.assertEqual(len(suggestions), 5)
        self.assertTrue(all(suggestion.startswith(str(i+1)) for i, suggestion in enumerate(suggestions)))
    
    def test_get_faq_suggestions_phone(self):
        input_text = "Mi celular no tiene señal."
        response = get_faq_suggestions(input_text)
        suggestions = response.split("\n")
        self.assertEqual(len(suggestions), 5)
        self.assertTrue(all(suggestion.startswith(str(i+1)) for i, suggestion in enumerate(suggestions)))
    
    def test_get_faq_suggestions_multiple_keywords(self):
        input_text = "Tengo problemas con el internet y el email."
        response = get_faq_suggestions(input_text)
        
        suggestions = response.split("\n")
        self.assertEqual(len(suggestions), 5)
        self.assertTrue(all(suggestion.startswith(str(i+1)) for i, suggestion in enumerate(suggestions)))
    
    def test_get_faq_suggestions_no_keywords(self):
        input_text = "Tengo un problema con la computadora."
        response = get_faq_suggestions(input_text)
        self.assertEqual(response, "No se encontraron sugerencias relacionadas con 'internet', 'red', 'email', 'telefono' o 'celular'.")
    
    @patch('random.sample')
    def test_get_faq_suggestions_randomness(self, mock_random_sample):
        mock_random_sample.return_value = [
            "Reinicia el router/modem: Apágalo, espera 10 segundos y enciéndelo nuevamente.",
            "Verifica el cableado: Asegúrate de que todos los cables estén bien conectados.",
            "Reinicia el PC: A veces un simple reinicio puede resolver problemas de conexión.",
            "Verifica el Wi-Fi: Asegúrate de estar conectado a la red correcta y con la contraseña adecuada.",
            "Comprueba si hay cortes de servicio: Contacta a tu proveedor de internet para verificar si hay interrupciones en tu área."
        ]
        
        input_text = "Tengo problemas con internet."
        response = get_faq_suggestions(input_text)
        
        suggestions = response.split("\n")
        self.assertEqual(len(suggestions), 5)
        self.assertTrue(all(suggestion.startswith(str(i+1)) for i, suggestion in enumerate(suggestions)))
        self.assertEqual(suggestions[0], "1. Reinicia el router/modem: Apágalo, espera 10 segundos y enciéndelo nuevamente.")
    
if __name__ == '__main__':
    unittest.main()