<?php
/**
 * Page du blog (reprend src/pages/blog/index.astro).
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>

<section class="blog-hero">
	<div class="wrap">
		<p class="eyebrow" style="text-align:left; margin-bottom: 12px;">Blog</p>
		<h1>Articles &amp; <span style="color: var(--gold)">Conseils</span></h1>
		<p>SEO, développement web, performance et stratégie digitale.</p>
	</div>
</section>

<section>
	<div class="wrap">
		<?php if ( have_posts() ) : ?>
			<?php echo pa_category_nav( null ); // phpcs:ignore ?>
			<div class="blog-full-grid">
				<?php
				$i = 0;
				while ( have_posts() ) {
					the_post();
					echo pa_post_card( get_post(), $i++ ); // phpcs:ignore
				}
				?>
			</div>
		<?php else : ?>
			<div style="text-align: center; padding: 48px 0; color: var(--muted);">
				<p style="font-size: 18px;">Aucun article pour le moment.</p>
			</div>
		<?php endif; ?>
	</div>
</section>

<?php
echo pa_newsletter_html(); // phpcs:ignore
get_footer();
