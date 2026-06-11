# Share the Flavor (Recipe-Sharing Application)

A modern, full-stack recipe-sharing platform where users can discover, create, edit, and delete their favorite recipes. Built with Django, the application features a premium culinary aesthetic, cinematic video backgrounds, and an AI-powered auto-tagger that analyzes recipe ingredients!

## Key Features

- **User Authentication:** Complete authentication system (Login, Registration, Logout) using `django-allauth`.
- **Full CRUD Functionality:** Users can seamlessly Add, Edit, View, and Delete their own recipes.
- **AI Dietary Auto-Tagging:** Automatically analyzes raw ingredients using Hugging Face's Zero-Shot NLP Classifier (`facebook/bart-large-mnli`) to intelligently assign dietary badges (e.g., Contains Meat, Vegan, Contains Gluten).
- **Cloudinary Storage:** All recipe images are securely stored and served via Cloudinary.

## AI Auditor Note
The first time you add or edit a recipe, the AI auditor will download the required NLP model from Hugging Face. This may take a minute depending on your internet connection, but subsequent classifications will be instantaneous.

## Built With
* [Django](https://www.djangoproject.com/) - Backend framework
* [Hugging Face Transformers](https://huggingface.co/) - AI Ingredient classification
* [Cloudinary](https://cloudinary.com/) - Image management
* [Bootstrap 5](https://getbootstrap.com/) & Vanilla CSS - Frontend styling

