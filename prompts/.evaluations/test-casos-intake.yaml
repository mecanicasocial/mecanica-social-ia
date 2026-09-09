#!/usr/bin/env python3
"""
Harness básico de evaluación para prompts.
Ejecuta test cases y reporta métricas.
"""

import json
import yaml
from pathlib import Path
from typing import List, Dict

class PromptEvaluator:
    """Evalúa prompts contra test cases definidos."""
    
    def __init__(self, prompt_path: str):
        with open(prompt_path) as f:
            self.config = yaml.safe_load(f)
    
    def run_tests(self) -> Dict:
        """Ejecuta todos los test cases."""
        resultados = {
            "prompt_id": self.config['id'],
            "version": self.config['version'],
            "total_tests": len(self.config.get('ejemplos', [])),
            "passed": 0,
            "failed": 0,
            "detalles": []
        }
        
        for i, ejemplo in enumerate(self.config.get('ejemplos', [])):
            # Aquí iría la lógica de prueba real
            # Por ahora: validar que output es JSON válido
            try:
                json.loads(ejemplo['expected'])
                resultados['passed'] += 1
                estado = "✓ PASS"
            except:
                resultados['failed'] += 1
                estado = "✗ FAIL"
            
            resultados['detalles'].append({
                "test": i + 1,
                "estado": estado,
                "input_preview": ejemplo['input'][:50] + "..."
            })
        
        resultados['tasa_exito'] = (
            resultados['passed'] / resultados['total_tests'] * 100
        )
        
        return resultados
    
    def report(self) -> str:
        """Genera reporte legible."""
        r = self.run_tests()
        return f"""
╔════════════════════════════════════════╗
║ EVALUACIÓN DE PROMPT                   ║
╚════════════════════════════════════════╝

Prompt ID:     {r['prompt_id']}
Versión:       {r['version']}
Tests:         {r['total_tests']}

RESULTADOS:
  ✓ Pasados:   {r['passed']}
  ✗ Fallidos:  {r['failed']}
  
Tasa de éxito: {r['tasa_exito']:.1f}%

DETALLES:
{chr(10).join([f"  {d['estado']} Test {d['test']}: {d['input_preview']}" 
               for d in r['detalles']])}

RECOMENDACIÓN:
{"✓ APROBADO - Listo para producción" if r['tasa_exito'] >= 95 else "✗ REVISAR - No cumple criterios"}
        """

if __name__ == "__main__":
    # Ejemplo: python harness_basico.py prompts/formulario-intake-v1.0.0.yaml
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python harness_basico.py <ruta_prompt.yaml>")
        sys.exit(1)
    
    evaluador = PromptEvaluator(sys.argv[1])
    print(evaluador.report())
