@default_seeds = (
	[0, 'human',
		['˭���',
		(
			'nou' => sub {
				$v = shift;
				print $v;
				return $v;
			}
		),
		100]
	]
);

1;
