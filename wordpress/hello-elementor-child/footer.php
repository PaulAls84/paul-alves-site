<?php
/**
 * Pied de page (reprend Footer.astro et MobileBar.astro).
 */

defined( 'ABSPATH' ) || exit;
?>
</main>

<footer class="site-footer">
	<div class="wrap">
		<div class="footer-grid">
			<div class="footer-col">
				<div class="footer-brand">
					<img src="<?php echo esc_url( pa_asset_url( 'logo-wordmark.webp' ) ); ?>" alt="Paul Alves" width="200" height="100" loading="lazy" />
				</div>
				<p style="color: rgba(255,255,255,.85); margin-bottom: 12px;">Développeur Web &amp; Consultant SEO</p>
				<p>J'aide les entreprises à se développer en ligne avec des solutions digitales performantes.</p>
				<div class="socials">
					<a href="https://linkedin.com/in/paul-alves" aria-label="LinkedIn" target="_blank" rel="noopener"><?php echo pa_svg( 'linkedin' ); // phpcs:ignore ?></a>
					<a href="https://twitter.com/paul_alves" aria-label="Twitter / X" target="_blank" rel="noopener"><?php echo pa_svg( 'x' ); // phpcs:ignore ?></a>
					<a href="https://github.com/PaulAls84" aria-label="GitHub" target="_blank" rel="noopener"><?php echo pa_svg( 'github' ); // phpcs:ignore ?></a>
					<a href="mailto:<?php echo esc_attr( PA_EMAIL ); ?>" aria-label="Email"><?php echo pa_svg( 'mail' ); // phpcs:ignore ?></a>
				</div>
			</div>

			<div class="footer-col">
				<h5>Navigation</h5>
				<ul>
					<li><a href="<?php echo esc_url( home_url( '/#accueil' ) ); ?>">Accueil</a></li>
					<li><a href="<?php echo esc_url( home_url( '/#services' ) ); ?>">Services</a></li>
					<li><a href="<?php echo esc_url( home_url( '/#apropos' ) ); ?>">À propos</a></li>
					<li><a href="<?php echo esc_url( home_url( '/#realisations' ) ); ?>">Réalisations</a></li>
					<li><a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>">Blog</a></li>
					<li><a href="<?php echo esc_url( home_url( '/#contact' ) ); ?>">Contact</a></li>
				</ul>
			</div>

			<div class="footer-col">
				<h5>Services</h5>
				<ul>
					<li><a href="<?php echo esc_url( home_url( '/#services' ) ); ?>">Développement Web</a></li>
					<li><a href="<?php echo esc_url( home_url( '/#services' ) ); ?>">Consultant SEO</a></li>
					<li><a href="<?php echo esc_url( home_url( '/#services' ) ); ?>">SEO Local</a></li>
					<li><a href="<?php echo esc_url( home_url( '/#services' ) ); ?>">Maintenance &amp; Support</a></li>
				</ul>
			</div>

			<div class="footer-col">
				<h5>Contact</h5>
				<div class="footer-contact">
					<div class="item"><?php echo pa_svg( 'mail', 18 ); // phpcs:ignore ?> <?php echo esc_html( PA_EMAIL ); ?></div>
					<div class="item"><?php echo pa_svg( 'phone', 18 ); // phpcs:ignore ?> <?php echo esc_html( PA_PHONE_DISPLAY ); ?></div>
					<div class="item"><?php echo pa_svg( 'pin', 18 ); // phpcs:ignore ?> Soissons, France</div>
				</div>
			</div>
		</div>

		<div class="copyright">
			<span>© <?php echo esc_html( gmdate( 'Y' ) ); ?> Paul Alves. Tous droits réservés</span>
			<span class="legal-links">
				<a href="<?php echo esc_url( home_url( '/mentions-legales/' ) ); ?>">Mentions légales</a>
				<a href="<?php echo esc_url( home_url( '/politique-confidentialite/' ) ); ?>">Confidentialité</a>
				<a href="<?php echo esc_url( home_url( '/plan-du-site/' ) ); ?>">Plan du site</a>
				<a href="#" class="cky-banner-element" data-cookie-prefs>Gérer les cookies</a>
			</span>
		</div>
	</div>
</footer>

<!-- Barre d'actions fixe (mobile uniquement) -->
<div id="mobile-bar" class="mobile-bar" aria-hidden="true" role="complementary" aria-label="Actions rapides">
	<a href="tel:<?php echo esc_attr( PA_PHONE ); ?>" class="mbar-btn mbar-call"><?php echo pa_svg( 'phone', 18 ); // phpcs:ignore ?> Appeler</a>
	<a href="#" <?php echo pa_cal_attrs(); // phpcs:ignore ?> class="mbar-btn mbar-book"><?php echo pa_svg( 'calendar', 18 ); // phpcs:ignore ?> Réserver</a>
</div>

<?php wp_footer(); ?>
</body>
</html>
