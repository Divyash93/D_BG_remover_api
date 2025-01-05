import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'

def test_api_health():
    """Test the API health endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/health')
        print("\n=== Health Check ===")
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Is it running?")
        return False

def test_api_info():
    """Test the API information endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/')
        print("\n=== API Information ===")
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Is it running?")
        return False

def test_remove_background(image_path):
    """Test the background removal endpoint"""
    try:
        print(f"\n=== Testing Background Removal with {image_path} ===")
        
        # Check if image file exists
        try:
            with open(image_path, 'rb') as image_file:
                files = {'image': image_file}
                
                print("Sending request to remove background...")
                response = requests.post(f'{BASE_URL}/remove-background', files=files)
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    # Generate output filename with timestamp
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    output_path = f'test_output_{timestamp}.png'
                    
                    # Save the processed image
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ Success! Background removed image saved as: {output_path}")
                    return True
                else:
                    print("❌ Error Response:", json.dumps(response.json(), indent=2))
                    return False
                
        except FileNotFoundError:
            print(f"❌ Error: Test image not found at {image_path}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API. Is it running?")
        return False

def test_invalid_file():
    """Test API response with invalid file type"""
    try:
        # Create a text file for testing
        test_file_path = 'test.txt'
        with open(test_file_path, 'w') as f:
            f.write('This is not an image')
        
        print("\n=== Testing Invalid File Type ===")
        with open(test_file_path, 'rb') as test_file:
            files = {'image': test_file}
            response = requests.post(f'{BASE_URL}/remove-background', files=files)
            
            print(f"Status Code: {response.status_code}")
            print("Response:", json.dumps(response.json(), indent=2))
        
        # Ensure the file is closed before attempting to delete it
        import os
        os.remove(test_file_path)
        
        return response.status_code == 400
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Is it running?")
        return False
    except PermissionError as e:
        print(f"PermissionError: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("🚀 Starting API Tests...")
    
    # Track test results
    results = {
        "health_check": test_api_health(),
        "api_info": test_api_info(),
        "invalid_file": test_invalid_file(),
        "background_removal": test_remove_background('test_image.jpg')
    }
    
    # Print summary
    print("\n=== Test Summary ===")
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    # Overall result
    all_passed = all(results.values())
    print(f"\nOverall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")

if __name__ == "__main__":
    run_all_tests() 