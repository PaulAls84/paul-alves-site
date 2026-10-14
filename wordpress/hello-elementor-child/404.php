<?php
/**
 * Page 404 (reprend src/pages/404.astro).
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>

<section class="nf-hero">
	<div class="wrap">
		<p class="eyebrow" style="text-align:left;">Erreur 404</p>
		<h1>Cette page n'existe pas (ou plus)</h1>
		<p class="lede">
			Le lien que vous avez suivi est peut-être cassé, ou la page a été déplacée.
			Pas de panique : tout le reste du site fonctionne très bien.
		</p>
		<div class="nf-actions">
			<a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="btn btn-gold">Retour à l'accueil</a>
			<a href="<?php echo esc_url( home_url( '/plan-du-site/' ) ); ?>" class="btn btn-outline">Voir le plan du site</a>
		</div>
	</div>
</section>

<section class="nf-links">
	<div class="wrap">
		<h2>Vous cherchiez peut-être…</h2>
		<ul class="nf-list">
			<li><a href="<?php echo esc_url( home_url( '/services/' ) ); ?>"><span class="nf-label">Services</span><span class="nf-desc">Création de site, refonte, SEO, maintenance, avec tarifs</span></a></li>
			<li><a href="<?php echo esc_url( home_url( '/realisations/' ) ); ?>"><span class="nf-label">Réalisations</span><span class="nf-desc">Projets clients et résultats obtenus</span></a></li>
			<li><a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>"><span class="nf-label">Blog</span><span class="nf-desc">Guides WordPress, SEO, hébergement et maintenance</span></a></li>
			<li><a href="<?php echo esc_url( home_url( '/a-propos/' ) ); ?>"><span class="nf-label">À propos</span><span class="nf-desc">Mon parcours et ma façon de travailler</span></a></li>
			<li><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><span class="nf-label">Contact</span><span class="nf-desc">Une question, un projet ? Parlons-en</span></a></li>
		</ul>
	</div>
</section>

<?php
get_footer();
