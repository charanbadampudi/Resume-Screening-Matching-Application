def check_imports():
    """Check if all required modules can be imported"""
    
    modules_to_check = [
        ('typing', ['Set', 'Dict', 'List', 'Tuple', 'Optional']),
        ('numpy', None),  # Changed: import numpy as a module, not specific items
        ('sklearn.feature_extraction.text', ['TfidfVectorizer']),
        ('sklearn.metrics.pairwise', ['cosine_similarity']),
        ('re', None),
        ('logging', None),
        ('PyPDF2', None),
        ('docx', None),  # Add python-docx check
        ('nltk', None),  # Add nltk check
        ('spacy', None),  # Add spacy check
    ]
    
    print("Checking imports...\n")
    
    for module_name, items in modules_to_check:
        try:
            if items:
                # Check if we can import specific items
                exec(f"from {module_name} import {', '.join(items)}")
                print(f"✅ Successfully imported {module_name} with {items}")
            else:
                # Just import the module
                exec(f"import {module_name}")
                print(f"✅ Successfully imported {module_name}")
        except ImportError as e:
            print(f"❌ Failed to import {module_name}: {e}")
            print(f"   Run: pip install {module_name}")
        except Exception as e:
            print(f"❌ Error with {module_name}: {e}")
    
    # Special check for numpy
    try:
        import numpy as np
        print("✅ Successfully imported numpy as np")
        print(f"   NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import numpy: {e}")
        print("   Run: pip install numpy")
    
    print("\n" + "="*50)
    print("Checking custom modules...\n")
    
    # Check custom modules
    custom_modules = [
        ('utils.text_processor', 'TextProcessor'),
        ('utils.resume_parser', 'ResumeParser'),
        ('utils.matcher', 'ResumeMatcher'),
        ('models.skill_extractor', 'SkillExtractor')
    ]
    
    for module_path, class_name in custom_modules:
        try:
            exec(f"from {module_path} import {class_name}")
            print(f"✅ {module_path} imported successfully")
        except ImportError as e:
            print(f"❌ {module_path} import failed: {e}")
        except Exception as e:
            print(f"❌ Error importing {module_path}: {e}")

if __name__ == "__main__":
    check_imports()