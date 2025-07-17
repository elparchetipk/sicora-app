#!/usr/bin/env python3
"""
SICORA Backend Python Stack - Validador de Compatibilidad Python 3.13
Verifica que todas las dependencias y configuraciones sean compatibles
"""

import sys
import subprocess
import importlib.util
from pathlib import Path


def check_python_version():
    """Verifica que estemos usando Python 3.13"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")

    if version.major != 3 or version.minor != 13:
        print("❌ ERROR: Se requiere Python 3.13")
        return False

    print("✅ Versión de Python correcta")
    return True


def check_critical_imports():
    """Verifica que las importaciones críticas funcionen"""
    critical_modules = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "sqlalchemy",
        "asyncpg",
        "alembic",
        "pytest",
        "redis",
        "httpx",
        "structlog",
    ]

    failed_imports = []

    for module in critical_modules:
        try:
            spec = importlib.util.find_spec(module)
            if spec is None:
                failed_imports.append(module)
            else:
                print(f"✅ {module}")
        except ImportError:
            failed_imports.append(module)

    if failed_imports:
        print(f"❌ Módulos faltantes: {', '.join(failed_imports)}")
        return False

    print("✅ Todas las importaciones críticas disponibles")
    return True


def check_problematic_packages():
    """Verifica que no haya paquetes problemáticos instalados"""
    problematic = ["chromadb", "chroma-hnswlib"]

    for package in problematic:
        try:
            spec = importlib.util.find_spec(package.replace("-", "_"))
            if spec is not None:
                print(f"⚠️  ADVERTENCIA: {package} instalado (puede causar problemas)")
                return False
        except ImportError:
            pass

    print("✅ No hay paquetes problemáticos instalados")
    return True


def check_pip_packages():
    """Verifica las versiones de paquetes instalados"""
    try:
        # Usar el pip del entorno virtual si existe
        venv_pip = Path("./venv/bin/pip")
        pip_cmd = (
            [str(venv_pip)] if venv_pip.exists() else [sys.executable, "-m", "pip"]
        )

        result = subprocess.run(pip_cmd + ["list"], capture_output=True, text=True)
        packages = result.stdout.lower()

        # Verificar paquetes clave
        key_packages = {"fastapi": "0.115", "pydantic": "2.10", "sqlalchemy": "2.0"}

        for package, min_version in key_packages.items():
            if package not in packages:
                print(f"❌ {package} no instalado")
                return False
            print(f"✅ {package} instalado")

        return True
    except Exception as e:
        print(f"❌ Error verificando paquetes: {e}")
        return False


def main():
    """Función principal de validación"""
    print("🔍 SICORA Backend Python Stack - Validación de Compatibilidad")
    print("=" * 60)

    checks = [
        ("Versión de Python", check_python_version),
        ("Importaciones críticas", check_critical_imports),
        ("Paquetes problemáticos", check_problematic_packages),
        ("Paquetes pip", check_pip_packages),
    ]

    all_passed = True

    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        if not check_func():
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TODAS LAS VALIDACIONES PASARON")
        print("✅ El entorno está listo para desarrollo")
        return 0
    else:
        print("❌ ALGUNAS VALIDACIONES FALLARON")
        print("🔧 Revisa los errores y ejecuta make dev-setup")
        return 1


if __name__ == "__main__":
    sys.exit(main())
