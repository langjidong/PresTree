library(ggtree)
library(treeio)

tree<-read.tree('herb.tree.fasta.treefile')
p <- ggtree(tree, branch.length = "none", layout = "rectangular") + geom_tiplab(fontface = 2, hjust = 1, geom = 'label')
ggsave('herb.tree.png', p, width = 10, height = 10)

tree<-read.tree('prescription.tree.fasta.treefile')
p <- ggtree(tree, branch.length = "none", layout = "rectangular") + geom_tiplab(fontface = 2, hjust = 1, geom = 'label')
ggsave('prescription.tree.png', p, width = 10, height = 10)
