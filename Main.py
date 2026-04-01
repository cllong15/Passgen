import string
import random
import re

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = string.punctuation

    def generate(self, length=12, use_uppercase=True, use_lowercase=True, 
                 use_digits=True, use_special=True, exclude_chars=""):
        """
        Generate a random password.
        
        Args:
            length (int): Length of the password (default: 12)
            use_uppercase (bool): Include uppercase letters (default: True)
            use_lowercase (bool): Include lowercase letters (default: True)
            use_digits (bool): Include digits (default: True)
            use_special (bool): Include special characters (default: True)
            exclude_chars (str): Characters to exclude from the password
            
        Returns:
            str: The generated password
        """
        # Build character pool
        char_pool = ""
        
        if use_lowercase:
            char_pool += self.lowercase
        if use_uppercase:
            char_pool += self.uppercase
        if use_digits:
            char_pool += self.digits
        if use_special:
            char_pool += self.special
        
        # Remove excluded characters
        for char in exclude_chars:
            char_pool = char_pool.replace(char, "")
        
        if not char_pool:
            raise ValueError("At least one character type must be enabled")
        
        # Generate password
        password = ''.join(random.choice(char_pool) for _ in range(length))
        return password

    def check_strength(self, password):
        """
        Check the strength of a password.
        
        Args:
            password (str): The password to check
            
        Returns:
            dict: Strength analysis with score and feedback
        """
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if re.search(r'[0-9]', password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            score += 1
        else:
            feedback.append("Add special characters")
        
        # Determine strength level
        if score <= 3:
            strength = "Weak"
        elif score <= 5:
            strength = "Fair"
        elif score <= 7:
            strength = "Good"
        else:
            strength = "Strong"
        
        return {
            "strength": strength,
            "score": score,
            "max_score": 8,
            "feedback": feedback
        }

    def generate_batch(self, count=5, length=12, **kwargs):
        """
        Generate multiple passwords at once.
        
        Args:
            count (int): Number of passwords to generate
            length (int): Length of each password
            **kwargs: Additional arguments for generate()
            
        Returns:
            list: List of generated passwords
        """
        return [self.generate(length, **kwargs) for _ in range(count)]


def main():
    """Main function with interactive menu."""
    generator = PasswordGenerator()
    
    print("=" * 50)
    print("       PASSWORD GENERATOR")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Generate a single password")
        print("2. Generate multiple passwords")
        print("3. Check password strength")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            try:
                length = input("Enter password length (default 12): ").strip()
                length = int(length) if length else 12
                
                use_upper = input("Include uppercase? (y/n, default y): ").strip().lower() != 'n'
                use_lower = input("Include lowercase? (y/n, default y): ").strip().lower() != 'n'
                use_digit = input("Include digits? (y/n, default y): ").strip().lower() != 'n'
                use_spec = input("Include special characters? (y/n, default y): ").strip().lower() != 'n'
                
                password = generator.generate(
                    length=length,
                    use_uppercase=use_upper,
                    use_lowercase=use_lower,
                    use_digits=use_digit,
                    use_special=use_spec
                )
                
                print(f"\nGenerated Password: {password}")
                
                strength = generator.check_strength(password)
                print(f"Strength: {strength['strength']} ({strength['score']}/{strength['max_score']})")
                
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            try:
                count = input("How many passwords? (default 5): ").strip()
                count = int(count) if count else 5
                length = input("Enter password length (default 12): ").strip()
                length = int(length) if length else 12
                
                passwords = generator.generate_batch(count=count, length=length)
                
                print(f"\nGenerated {count} passwords:")
                for i, pwd in enumerate(passwords, 1):
                    print(f"{i}. {pwd}")
                
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            password = input("Enter password to check: ").strip()
            if password:
                strength = generator.check_strength(password)
                print(f"\nPassword Strength: {strength['strength']}")
                print(f"Score: {strength['score']}/{strength['max_score']}")
                if strength['feedback']:
                    print("Suggestions:")
                    for suggestion in strength['feedback']:
                        print(f"  - {suggestion}")
            else:
                print("No password entered.")
        
        elif choice == "4":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
