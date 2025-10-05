# FortiQode

FortiQode is a QR-like encrypted image generator that hides secret messages inside a custom 100×100 grid.<br>
Unlike standard QR codes, this system:

<ul>
<li>Uses symmetric encryption (Fernet/AES) to secure messages.</li>
<li>Embeds binary ciphertext into the grid while skipping orientation zones.</li>
<li>Fills unused cells with random noise (gibberish) to mimic a QR code.</li>
<li>Provides a custom extraction and decryption routine to recover the original message.</li>
</ul>

---

<h3>Features</h3>
<ul>
<li>Symmetric encryption using <a href="https://cryptography.io/en/latest/">cryptography</a> (`Fernet`).</li>
<li>QR-like design with orientation squares and white borders.</li>
<li>Secure embedding of binary ciphertext.</li>
<li>Decryption script to extract hidden messages.</li>
<li>Easily extendable (mobile scanning, error correction, etc.).</li>
</ul>

---

<h3>Requirements</h3>
<ul>
<li>Python 3.8+ recommended.</li>
<li>Install dependencies using pip:</li>
</ul>

<pre>
pip install matplotlib numpy cryptography python-docx
</pre>

---

<h3>Usage</h3>

<b>1. Generate an Encrypted QR-like Image</b>

<pre>
python encrypt_qr.py
</pre>

<ul>
<li>Enter your secret text (≤192 characters).</li>
<li>The script will:</li>
<ul>
<li>Generate a symmetric key.</li>
<li>Encrypt the text.</li>
<li>Embed it into a 100×100 QR-like matrix.</li>
<li>Save an image as <code>qr_like_encrypted.png</code>.</li>
</ul>
</ul>

Output example:

<pre>
Generated Symmetric Key (store safely): vHyJ3Wm8H8x2...==
Image saved as: qr_like_encrypted.png
</pre>

Note: Save the key securely — it is required for decryption.

---

<b>2. Extract & Decrypt the Message</b>

<pre>
python decrypt_qr.py
</pre>

<ul>
<li>Load the <code>qr_like_encrypted.png</code>.</li>
<li>Extract binary data, skipping orientation zones.</li>
<li>Reconstruct the encrypted ciphertext.</li>
<li>Decrypt it using the same symmetric key.</li>
</ul>

Output example:

<pre>
Extracted & Decrypted Message:
Hello World
</pre>

---

<h3>Optional Improvements</h3>
<ul>
<li>Integration with mobile apps for scanning and automatic decryption.</li>
<li>Error correction to improve robustness.</li>
<li>Dynamic scaling for larger messages.</li>
<li>Support for multiple encryption schemes or multi-layer encryption.</li>
</ul>

---

<h3>Libraries Used</h3>
<ul>
<li><code>matplotlib</code>: Displaying and saving QR-like images.</li>
<li><code>numpy</code>: Matrix operations for the QR-like grid.</li>
<li><code>random</code>: Fill unused cells with noise.</li>
<li><code>cryptography (Fernet)</code>: Symmetric encryption and decryption.</li>
<li><code>python-docx</code>: (Optional) Generate documentation reports.</li>
</ul>

---

<h3>Example Use Cases</h3>
<ul>
<li>Securely sharing confidential messages.</li>
<li>Offline secure messaging using printed QR-like images.</li>
<li>Multi-factor authentication where the image acts as a secure token.</li>
<li>Secure event tickets distributed as encrypted QR-like codes.</li>
<li>Educational tool for cryptography and steganography learning.</li>
</ul>
