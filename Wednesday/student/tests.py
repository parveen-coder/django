from django.test import TestCase
from django.urls import reverse
# Create your tests here.









class HomeTest(TestCase):
    def testview(self):
        response=self.client.get('/student/divide/')
        # self.assertEqual(response.status_code,200)
        self.assertTrue(response.status_code == 200)
        # self.assertEqual(response, 'result')
        # self.assertContains(response, 'result')
        self.assertContains(response, '10.0')
        # self.assertTemplateUsed(response, "result.html" )

       
       
       
       

       
       




     
       

    def test_home3(self):
        response = self.client.get('/student/home3/',{'name':'Rohit'})
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, "Hello how are you")
        # self.assertTrue("Rohit" in response.content.decode())
        # self.assertContains(response, "Rohit")

# class ErrorTest(TestCase):

#     def test_invalid_url(self):

#         response = self.client.get('/student/newstudent/')
#         # self.assertEqual(response.status_code,404)
#         self.assertEqual(response.status_code,200)

def test_student_detail_view(self):
    response = self.client.get(
        reverse("student_detail", args=[10])
    )

    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "10")