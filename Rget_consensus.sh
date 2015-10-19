#Error capture mode set to strict.

set -ue

#samtools view -bT phage-lambda.fa pass.sam > pass.bam
#samtools sort pass.bam pass_sorted
#samtools index pass_sorted.bam

OUT=output_reads

Index=5000
Increment=5000
while [ $Index -le 48000 ]
do
echo "Extracting reads overlapping base $Index in reference"
#samtools view -h pass_sorted.bam "gi|215104|gb|J02459.1|LAMCG":$i-$i | samtools bam2fq - | seqtk seq -a | clustalo -i - --outfmt=clu > New_reads/out_aln_${i}.clu
samtools view -h -f 16 pass_sorted.bam "gi|215104|gb|J02459.1|LAMCG":$Index-$Index | samtools bam2fq - | seqtk seq -a | seqtk seq -r > Reads.fa
samtools view -h -F 20 pass_sorted.bam "gi|215104|gb|J02459.1|LAMCG":$Index-$Index | samtools bam2fq - | seqtk seq -a >> Reads.fa
#MSA
echo "Performing the Multiple Sequence Alignment"
clustalo -i Reads.fa --outfmt=clu > MSAs/Alignment_${Index}.clu
echo "python construct_consensus.py MSAs/Alignment_${Index}.clu $OUT"
python construct_consensus.py MSAs/Alignment_${Index}.clu $OUT.fa
#incrementing index
Index=$(($Index+$Increment))
done

#bwa index phage-lambda.fa
#Takes one command line input

cd References
bwa mem -X ont2d phage-lambda.fa $OUT.fa > ../Output_reads/${OUT}_aligned.sam
cd ..
samtools view -bS Output_reads/${OUT}_aligned.sam > Output_reads/${OUT}_aligned.bam
samtools sort Output_reads/${OUT}_aligned.bam Output_reads/${OUT}_sorted
samtools index Output_reads/${OUT}_sorted.bam

#Done.
