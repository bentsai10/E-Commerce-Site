# Quaranthings
Social e-commerce site allowing users to "purchase" appointments or DIY items from friends for quarantine activities to do together

<p align = "center"><kbd><img src = "/images/home.png"></kbd></p>

<p><strong>Quaranthings' purpose:</strong><br> 
Connect users through activity appointments scheduled with intentionality and DIY items during isolated periods of quarantining</p>

<h3> Accessing Quaranthings</h3>
<ul>
  <li>Download this project from Github</li>
  <li>Make sure you have python3 installed</li>
  <li>Create a virtual environment and pip install django==2.2</li>
  <li>Navigate to project level folder in terminal and run "python manage.py runserver"</li>
  <li>Go to http://localhost:8000/ in your desired browser!</li>
  <li>Enjoy Quaranthings!</li>
  <li>(Deployment coming soon...)</li>
</ul>

<h3>How Quaranthings Works</h3>
<ol>
  <li>Login/Register to join the Quarangiver community to post Quaranthings, leave reviews, or add Quaranthings to your cart</li>
  <br>
  <p align = "center"><kbd><img src = "/images/login_register_pages.gif"></kbd></p>
 <li>Both the login/register pages are equipped with validations to ensure data congruency</li>
  <br>
 <p align = "center"><kbd><img src = "/images/register_validations.gif"></kbd></p>
 <p align = "center"><kbd><img src = "/images/login_validations.gif"></kbd></p>
  <li>Once logged in, you have access to your profile, your orders, and your own cart!</li>
  <br>
 <p align = "center"><kbd><img src = "/images/successful_login.gif"></kbd></p>
  <li>Navigate to the Top Picks page to see the most popular items other Quarangivers have posted</li>
  <br>
  <p align = "center"><kbd><img src = "/images/top_picks.gif"></kbd></p>
  <li>The top picks page is equipped with AJAX filtering fictions, allowing you to narrow down your search</li>
  <br>
  <p align = "center"><kbd><img src = "/images/ajax_filtering.gif"></kbd></p>
  <li>If you want to see Quaranthings in a specific category, just navigate to that category's page</li>
  <br>
  <p align = "center"><kbd><img src = "/images/categories.gif"></kbd></p>
  <li>To take an in depth look at a Quaranthing, click on the Quaranthing card. On the Quaranthing page, you can see other images of the Quaranthing, add it to your cart, leave a review, or see related items</li>
  <br>
  <p align = "center"><kbd><img src = "/images/quaranthing.gif"></kbd></p>
  <p align = "center"><kbd><img src = "/images/quaranthing_photos.gif"></kbd></p>
  <p align = "center"><kbd><img src = "/images/review.gif"></kbd></p>
  <li>To find others in the Quarangivers community, navigate to the Quarangivers page</li>
  <br>
  <p align = "center"><kbd><img src = "/images/quarangivers.gif"></kbd></p>
  <p align = "center"><kbd><img src = "/images/quarangiver.gif"></kbd></p>
  <li>To personalize your quarangiver profile, go to edit profile to add a profile pic</li>
  <br>
  <p align = "center"><kbd><img src = "/images/edit_profile.gif"></kbd></p>
  <li>To list your own Quaranthing, go to Post Quaranthings</li>
  <br>
  <p align = "center"><kbd><img src = "/images/new_listing.gif"></kbd></p>
  <p align = "center"><kbd><img src = "/images/new_listing_process.gif"></kbd></p>
  <li>Coming Soon...</li>
  <br>
  <ul>
    <li>Responsive layout</li>
    <li>Search bar</li>
  </ul>
</ol>
<h3>Logic Behind Quaranthings</h3>
<ul>
  <li>OrderItem Model & Cart</li>
  <ul>
    <li>Needed to create OrderItem model separate from Product model (but essentially serving same purpose) to store desired quantity for product</li>
    <li>There is also no cart object. Simply, the cart is the only unordered order (ordered = False) associated with a user</li>
    <li>If no unordered orders exist, a new one is created when a user adds an item to the cart</li>
  </ul>
  
```python3
class Order(models.Model):
    products = models.ManyToManyField(OrderItem)
    user = models.ForeignKey(User, related_name = "orders", on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
  <li>Register/Login/Change Password validators</li>
  <ul>
    <li>Worked with datetime to ensure only users 13 and older can sign up for an account (enables giving user promotional deals when it's their birthday in the future)</li>
    <li>Used EMAIL_REGEX to verify proper email format</li>
    <li>Used bcrypt to encrypt user password</li>
  </ul>
  
```python3
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        try:
            birthdate = datetime.strptime(postData["birthday"], '%Y-%m-%d').date()
        except ValueError:
            birthdate = date.today()
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters!"
        if (date.today()-birthdate).days < 4745: #365 * 13
            errors["birthday"] = "Your need to be at least 13 years old to create an account!"
        if birthdate >= date.today():
            errors["birthday"] = "Your birthday needs to be in the past!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email = postData['email'].lower()).all().count() > 0:
            errors['email'] = "An account already exists with this email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if postData['password'] != postData['password_conf']:
            errors['password'] = "Your passwords don't match!"
        return errors
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
            return errors
        lower_email = postData['email'].lower()
        user = User.objects.filter(email=lower_email) 
        if user:
            logged_user = user[0] 
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors["password"] = "Incorrect password!"
        else:
            errors["email"] = "This email has not been registered!"
        return errors
    def password_validator(self, postData):
        errors = {}
        lower_email = postData['email'].lower()
        user = User.objects.filter(email=lower_email)[0]
        if not bcrypt.checkpw(postData['old_pw'].encode(), user.password.encode()):
            errors["old_pw"] = "Your previous password is incorrect!"
        if len(postData['new_pw']) < 8:
            errors['new_pw'] = "New password must be at least 8 characters!"
        if postData['new_pw_conf'] != postData['new_pw']:
            errors['new_pw_conf'] = "Your new passwords don't match!"
        return errors
```
  <li>Add to Cart function</li>
  <ul>
    <li>Retrieve User cart and desired item to be added to cart</li>
    <li>If the product already exists in the cart, add the newly inputted quantity to the quantity already in the cart</li>
    <li>Otherwise, create a new OrderItem object linked to this product and add it to the cart</li>
  </ul>

```python3
def add_to_cart(request, num):
    if request.method == "POST":
        user = User.objects.filter(email = request.session['logged_user']).all().first()
        #if user does have a cart, find it. Otherwise create a new cart
        if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
            cart = Order.objects.filter(user = user).filter(ordered = False).all().first()
        else:
            cart = Order.objects.create(user = user, total = 0)
        
        product = Product.objects.get(id = num)

        
        exists = False
        #if product to be added to cart already exists in cart
        for item in cart.products.all():
            if item.product ==  product:
                item.quantity += int(request.POST['quantity'])
                item.save()
                cart.total += int(request.POST['quantity']) * item.product.price
                cart.save()
                exists = True
        if not exists:
            new_item = OrderItem.objects.create(product = product, quantity = request.POST['quantity'])
            cart.products.add(new_item)
            cart.total += Decimal(new_item.quantity) * Decimal(new_item.product.price)
            cart.save()
        return redirect('/users/cart')
    else:
        return redirect('/quaranthings/{}'.format(num))
```
</ul>
