<?php
/**
 * Catégorie du blog (reprend src/pages/blog/categorie/[categorie].astro).
 */

defined( 'ABSPATH' ) || exit;

get_header();
$term = get_queried_object();
?>

<section class="blog-hero">
	<div class="wrap">
		<p class="eyebrow" style="text-align:left; margin-bottom: 12px;">Catégorie</p>
		<h1><?php echo esc_html( $term->name ); ?></h1>
		<p>Tous les articles de la catégorie <?php echo esc_html( $term->name ); ?>.</p>
	</div>
</section>

<section>
	<div class="wrap">
		<?php echo pa_category_nav( $term->slug ); // phpcs:ignore ?>
		<div class="blog-full-grid">
			<?php
			$i = 0;
			while ( have_posts() ) {
				the_post();
				echo pa_post_card( get_post(), $i++ ); // phpcs:ignore
			}
			?>
		</div>
	</div>
</section>

<?php
echo pa_newsletter_html(); // phpcs:ignore
get_footer();
