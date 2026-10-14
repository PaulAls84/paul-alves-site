<?php
/**
 * En-tête du site (reprend Nav.astro).
 */

defined( 'ABSPATH' ) || exit;

$blog_active = is_home() || is_singular( 'post' ) || is_category();
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip-link screen-reader-text" href="#contenu">Aller au contenu</a>

<header class="nav" id="nav">
	<div class="wrap nav-inner">
		<a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="brand" aria-label="Paul Alves, accueil">
			<img src="<?php echo esc_url( pa_asset_url( 'logo-wordmark.webp' ) ); ?>" alt="Paul Alves" width="200" height="100" />
		</a>

		<nav class="nav-links" id="navLinks">
			<?php
			echo pa_nav_link( home_url( '/#accueil' ), 'Accueil', is_front_page() ); // phpcs:ignore
			echo pa_nav_link( home_url( '/services/' ), 'Services', is_page( 'services' ) ); // phpcs:ignore
			echo pa_nav_link( home_url( '/a-propos/' ), 'À propos', is_page( 'a-propos' ) ); // phpcs:ignore
			echo pa_nav_link( home_url( '/realisations/' ), 'Réalisations', is_page( 'realisations' ) ); // phpcs:ignore
			echo pa_nav_link( home_url( '/blog/' ), 'Blog', $blog_active ); // phpcs:ignore
			echo pa_nav_link( home_url( '/contact/' ), 'Contact', is_page( 'contact' ) ); // phpcs:ignore
			?>
			<div class="nav-mobile-ctas">
				<a href="#" <?php echo pa_cal_attrs(); // phpcs:ignore ?> class="btn btn-gold nav-mobile-book">Réserver un appel gratuit</a>
				<a href="tel:<?php echo esc_attr( PA_PHONE ); ?>" class="btn btn-outline nav-mobile-call">
					<?php echo pa_svg( 'phone' ); // phpcs:ignore ?>
					<?php echo esc_html( PA_PHONE_DISPLAY ); ?>
				</a>
			</div>
		</nav>

		<a href="#" <?php echo pa_cal_attrs(); // phpcs:ignore ?> class="btn btn-navy nav-cta-desktop">Prendre rendez-vous</a>

		<button class="mobile-toggle" id="mobileToggle" aria-label="Ouvrir le menu">
			<span></span><span></span><span></span>
		</button>
	</div>
</header>
<main id="contenu">
