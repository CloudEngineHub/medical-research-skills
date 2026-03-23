#!/usr/bin/env python3
"""Vector Text Fixer - Fix garbled text in PDF/SVG vector images"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict


@dataclass
class TextBlock:
    """text block data structure"""
    id: str
    bbox: List[float]  # [x0, y0, x1, y1]
    original_text: str
    page_num: int = 1
    font_info: Dict[str, Any] = None
    confidence: float = 1.0
    suggested_fix: str = ""
    is_garbled: bool = False


class GarbledTextDetector:
    """Garbled text detector"""
    
    # Common gibberish/replacement characters
    REPLACEMENT_CHARS = {
        '\ufffd',  # � Replacement character
        '\u25a1',  # □ box
        '\u25a0',  # ■ Solid box
        '\u25af',  # ▯ hollow square
        '\u2588',  # █ Whole block
        '\ufffe',  # � non-character
        '\uffff',  # � non-character
        '?',       # question mark substitution
    }
    
    # Common garbled patterns
    GARBLED_PATTERNS = [
        r'[\u0000-\u0008\u000b-\u000c\u000e-\u001f]',  # control characters
        r'[\ufffd\u25a1\u25a0\u25af\u2588\ufffe\uffff]',  # Replace character
        r'[�]{2,}',  # Continuous replacement characters
        r'(?:\\x[0-9a-fA-F]{2}){2,}',  # escape sequence
        r'[\x80-\x9f]',  # C1 control character
    ]
    
    def __init__(self):
        self.compiled_patterns = [re.compile(p) for p in self.GARBLED_PATTERNS]
    
    def is_garbled(self, text: str) -> Tuple[bool, float]:
        """Detect whether text is garbled
        Return: (Whether it is garbled, garbled confidence level 0-1)"""
        if not text or not isinstance(text, str):
            return False, 1.0
        
        text_len = len(text)
        if text_len == 0:
            return False, 1.0
        
        garbled_score = 0.0
        
        # 1. Check for replacement characters
        replacement_count = sum(1 for c in text if c in self.REPLACEMENT_CHARS)
        garbled_score += (replacement_count / text_len) * 0.5
        
        # 2. Check the garbled code pattern
        for pattern in self.compiled_patterns:
            matches = pattern.findall(text)
            if matches:
                garbled_score += len(matches) / text_len * 0.3
        
        # 3. Check for abnormal character distribution
        if self._has_abnormal_distribution(text):
            garbled_score += 0.2
        
        # 4. Check for signs of mixed encoding
        if self._has_encoding_mixed(text):
            garbled_score += 0.15
        
        is_garbled = garbled_score > 0.15 or replacement_count > 0
        confidence = max(0.0, 1.0 - min(garbled_score, 1.0))
        
        return is_garbled, confidence
    
    def _has_abnormal_distribution(self, text: str) -> bool:
        """Check whether the character distribution is abnormal"""
        if len(text) < 3:
            return False
        
        # Statistical proportion of unprintable characters
        unprintable = sum(1 for c in text if ord(c) < 32 and c not in '\t\n\r')
        ratio = unprintable / len(text)
        return ratio > 0.3
    
    def _has_encoding_mixed(self, text: str) -> bool:
        """Detecting signs of mixed encoding"""
        # Detecting signs that UTF-8 multibyte characters are being parsed incorrectly
        # For example: é should be é (UTF-8 bytes are parsed as Latin-1)
        mixed_patterns = [
            r'Ã[\xa0-\xbf]',  # UTF-8 misparsed as Latin-1
            r'Â[\x80-\xbf]',
            r'Ã¢',
            r'Ã£',
        ]
        for pattern in mixed_patterns:
            if re.search(pattern, text):
                return True
        return False


class PDFFixer:
    """PDF text repairer"""
    
    def __init__(self, detector: GarbledTextDetector):
        self.detector = detector
        self.text_blocks: List[TextBlock] = []
    
    def fix(self, input_path: str, output_path: str, 
            repair_level: str = "standard") -> Dict[str, Any]:
        """Fix garbled text in PDF files"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            return {
                "success": False,
                "error": "PyMuPDF (fitz) is required. Install: pip install PyMuPDF"
            }
        
        try:
            doc = fitz.open(input_path)
        except Exception as e:
            return {"success": False, "error": f"Cannot open PDF: {str(e)}"}
        
        self.text_blocks = []
        repair_count = 0
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = self._extract_text_blocks(page, page_num + 1)
            
            for block in blocks:
                is_garbled, confidence = self.detector.is_garbled(block.original_text)
                
                if is_garbled:
                    block.is_garbled = True
                    block.confidence = confidence
                    block.suggested_fix = self._suggest_fix(
                        block.original_text, 
                        repair_level
                    )
                    repair_count += 1
                
                self.text_blocks.append(block)
        
        # Generate repair report
        result = {
            "success": True,
            "file_type": "pdf",
            "pages": len(doc),
            "total_blocks": len(self.text_blocks),
            "garbled_blocks": repair_count,
            "text_blocks": [asdict(b) for b in self.text_blocks],
            "output_path": output_path
        }
        
        doc.close()
        return result
    
    def _extract_text_blocks(self, page, page_num: int) -> List[TextBlock]:
        """Extract text blocks from PDF pages"""
        blocks = []
        
        try:
            import fitz
            
            # Get the text block on the page
            text_dict = page.get_text("dict")
            
            block_id = 0
            for block in text_dict.get("blocks", []):
                if "lines" in block:  # text block
                    for line in block["lines"]:
                        for span in line.get("spans", []):
                            text = span.get("text", "")
                            if text.strip():
                                bbox = span.get("bbox", [0, 0, 0, 0])
                                font_info = {
                                    "font": span.get("font", "Unknown"),
                                    "size": span.get("size", 0),
                                    "flags": span.get("flags", 0),
                                    "color": span.get("color", 0)
                                }
                                
                                tb = TextBlock(
                                    id=f"p{page_num}_b{block_id}",
                                    bbox=list(bbox),
                                    original_text=text,
                                    page_num=page_num,
                                    font_info=font_info
                                )
                                blocks.append(tb)
                                block_id += 1
        except Exception as e:
            print(f"Warning: Error extracting text: {e}")
        
        return blocks
    
    def _suggest_fix(self, garbled_text: str, repair_level: str) -> str:
        """Suggest repairing text based on garbled content"""
        # More complex repair logic can be implemented here
        # Currently returns a placeholder, prompting the user to enter manually
        
        if repair_level == "minimal":
            # Minimal fix: only remove replacement characters
            return garbled_text.replace('\ufffd', '').strip()
        
        elif repair_level == "aggressive":
            # Deep Fix: Try decoding common encoding errors
            return self._try_decode_fixes(garbled_text)
        
        else:  # standard
            # Standard fix: Marking requires user confirmation
            if all(c in GarbledTextDetector.REPLACEMENT_CHARS for c in garbled_text):
                return f"[Need to enter manually - original: {len(garbled_text)}garbled characters]"
            else:
                return garbled_text.replace('\ufffd', '[?]').strip()
    
    def _try_decode_fixes(self, text: str) -> str:
        """Try multiple encoding fixes"""
        # Common coding error pattern fixes
        fixes = []
        
        # UTF-8 is parsed as Latin-1
        try:
            fixed = text.encode('latin-1').decode('utf-8')
            fixes.append(fixed)
        except:
            pass
        
        # GBK/GB2312 problem
        try:
            fixed = text.encode('latin-1').decode('gbk', errors='ignore')
            fixes.append(fixed)
        except:
            pass
        
        # Return the first fix that looks reasonable
        for fix in fixes:
            if not self.detector.is_garbled(fix)[0]:
                return fix
        
        return f"[Need to enter manually]"


class SVGFixer:
    """SVG text fixer"""
    
    def __init__(self, detector: GarbledTextDetector):
        self.detector = detector
        self.text_elements: List[TextBlock] = []
    
    def fix(self, input_path: str, output_path: str,
            repair_level: str = "standard") -> Dict[str, Any]:
        """Fix garbled text in SVG files"""
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            return {
                "success": False,
                "error": "BeautifulSoup4 is required. Install: pip install beautifulsoup4"
            }
        
        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {"success": False, "error": f"Cannot read SVG: {str(e)}"}
        
        soup = BeautifulSoup(content, 'xml')
        
        # Extract all text elements
        self.text_elements = []
        repair_count = 0
        
        text_tags = soup.find_all(['text', 'tspan', 'textPath'])
        
        for idx, tag in enumerate(text_tags):
            text_content = tag.get_text()
            if not text_content.strip():
                continue
            
            is_garbled, confidence = self.detector.is_garbled(text_content)
            
            # Get location and font information
            x = tag.get('x', '0')
            y = tag.get('y', '0')
            font_family = tag.get('font-family', 'default')
            font_size = tag.get('font-size', '12')
            
            tb = TextBlock(
                id=f"text_{idx}",
                bbox=[float(x) if x else 0, float(y) if y else 0, 0, 0],
                original_text=text_content,
                font_info={
                    "font_family": font_family,
                    "font_size": font_size
                },
                page_num=1
            )
            
            if is_garbled:
                tb.is_garbled = True
                tb.confidence = confidence
                tb.suggested_fix = self._suggest_fix(text_content, repair_level)
                repair_count += 1
            
            self.text_elements.append(tb)
        
        # Get basic information about SVG
        svg_tag = soup.find('svg')
        svg_info = {
            "width": svg_tag.get('width', 'unknown') if svg_tag else 'unknown',
            "height": svg_tag.get('height', 'unknown') if svg_tag else 'unknown',
            "viewBox": svg_tag.get('viewBox', '') if svg_tag else ''
        }
        
        result = {
            "success": True,
            "file_type": "svg",
            "svg_info": svg_info,
            "total_elements": len(self.text_elements),
            "garbled_elements": repair_count,
            "text_elements": [asdict(t) for t in self.text_elements],
            "output_path": output_path
        }
        
        return result
    
    def _suggest_fix(self, garbled_text: str, repair_level: str) -> str:
        """Suggested SVG text fixes"""
        if repair_level == "minimal":
            return garbled_text.replace('\ufffd', '').strip()
        elif repair_level == "aggressive":
            return self._try_xml_entity_fix(garbled_text)
        else:
            if '\ufffd' in garbled_text:
                return f"[Need to enter manually - original: {len(garbled_text)}garbled characters]"
            return garbled_text
    
    def _try_xml_entity_fix(self, text: str) -> str:
        """Try to fix XML entity encoding issue"""
        import html
        # Decode HTML entities
        decoded = html.unescape(text)
        if not self.detector.is_garbled(decoded)[0]:
            return decoded
        return f"[Need to enter manually]"


class VectorTextFixer:
    """Vector text fixer main class"""
    
    def __init__(self):
        self.detector = GarbledTextDetector()
        self.pdf_fixer = PDFFixer(self.detector)
        self.svg_fixer = SVGFixer(self.detector)
    
    def fix_file(self, input_path: str, output_path: str,
                 repair_level: str = "standard") -> Dict[str, Any]:
        """Automatically select repair method based on file type"""
        input_path = Path(input_path)
        
        if not input_path.exists():
            return {"success": False, "error": f"File not found: {input_path}"}
        
        suffix = input_path.suffix.lower()
        
        if suffix == '.pdf':
            return self.pdf_fixer.fix(str(input_path), output_path, repair_level)
        elif suffix == '.svg':
            return self.svg_fixer.fix(str(input_path), output_path, repair_level)
        else:
            return {"success": False, "error": f"Unsupported file format: {suffix}"}
    
    def batch_fix(self, input_folder: str, output_folder: str,
                  repair_level: str = "standard") -> List[Dict[str, Any]]:
        """Batch repair PDF/SVG files in folders"""
        input_folder = Path(input_folder)
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        for file_path in input_folder.iterdir():
            if file_path.suffix.lower() in ['.pdf', '.svg']:
                output_path = output_folder / f"fixed_{file_path.name}"
                result = self.fix_file(str(file_path), str(output_path), repair_level)
                results.append(result)
        
        return results
    
    def export_editable_json(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """Export editable JSON format for manual repair in AI tools"""
        result = self.fix_file(input_path, "", repair_level="standard")
        
        if not result.get("success"):
            return result
        
        # Add editable markup
        editable_data = {
            "file_info": {
                "original_path": input_path,
                "exported_at": self._get_timestamp(),
                "tool": "Vector Text Fixer v1.0.0"
            },
            "repair_data": result
        }
        
        # Add user editable fields
        if result["file_type"] == "pdf":
            for block in editable_data["repair_data"]["text_blocks"]:
                block["user_editable"] = block.get("suggested_fix", "")
        elif result["file_type"] == "svg":
            for elem in editable_data["repair_data"]["text_elements"]:
                elem["user_editable"] = elem.get("suggested_fix", "")
        
        # Save JSON
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(editable_data, f, ensure_ascii=False, indent=2)
            editable_data["export_success"] = True
        except Exception as e:
            editable_data["export_success"] = False
            editable_data["export_error"] = str(e)
        
        return editable_data
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(
        description='Vector Text Fixer - Fix garbled text in PDF/SVG vector images'
    )
    
    # Enter options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', '-i', help='Enter file path (PDF or SVG)')
    input_group.add_argument('--batch', '-b', help='Batch process input folders')
    
    # Output options
    parser.add_argument('--output', '-o', help='Output file/folder path')
    parser.add_argument('--export-json', '-j', help='Export editable JSON format')
    
    # Repair options
    parser.add_argument('--repair-level', '-r', 
                       choices=['minimal', 'standard', 'aggressive'],
                       default='standard',
                       help='Repair level (default: standard)')
    parser.add_argument('--interactive', action='store_true',
                       help='Enable interactive repair mode')
    
    args = parser.parse_args()
    
    # Create a fixer instance
    fixer = VectorTextFixer()
    
    # Export JSON schema
    if args.export_json:
        if not args.input:
            print("Error: --export-json requires specifying --input")
            sys.exit(1)
        
        result = fixer.export_editable_json(args.input, args.export_json)
        
        if result.get("export_success"):
            print(f"✓ JSONExport successful: {args.export_json}")
            print(f"  File type: {result['repair_data'].get('file_type')}")
            print(f"  Detected text block: {result['repair_data'].get('total_blocks') or result['repair_data'].get('total_elements')}")
            print(f"  Garbled text block: {result['repair_data'].get('garbled_blocks') or result['repair_data'].get('garbled_elements')}")
        else:
            print(f"✗ Export failed: {result.get('export_error', 'Unknown error')}")
            sys.exit(1)
        return
    
    # batch processing mode
    if args.batch:
        if not args.output:
            print("Error: Batch processing requires specifying --output")
            sys.exit(1)
        
        print(f"Start batch processing: {args.batch}")
        results = fixer.batch_fix(args.batch, args.output, args.repair_level)
        
        success_count = sum(1 for r in results if r.get("success"))
        total_count = len(results)
        
        print(f"\nProcessing completed: {success_count}/{total_count} File successful")
        for r in results:
            if r.get("success"):
                garbled = r.get("garbled_blocks") or r.get("garbled_elements", 0)
                print(f"  ✓ {r.get('output_path')} (English: {garbled})")
            else:
                print(f"  ✗ {r.get('error', 'Unknown error')}")
        return
    
    # Single file processing mode
    if args.input:
        print(f"Process files: {args.input}")
        
        result = fixer.fix_file(args.input, args.output or "", args.repair_level)
        
        if result.get("success"):
            print(f"✓ Analysis completed")
            print(f"  File type: {result.get('file_type')}")
            
            if result.get('file_type') == 'pdf':
                print(f"  Number of pages: {result.get('pages')}")
                print(f"  text block: {result.get('total_blocks')}")
                print(f"  Garbled blocks: {result.get('garbled_blocks')}")
            else:
                print(f"  text element: {result.get('total_elements')}")
                print(f"  Garbled elements: {result.get('garbled_elements')}")
            
            # Show garbled text details
            blocks = result.get('text_blocks') or result.get('text_elements', [])
            garbled_blocks = [b for b in blocks if b.get('is_garbled')]
            
            if garbled_blocks:
                print(f"\nGarbled text detected:")
                for i, block in enumerate(garbled_blocks[:5], 1):
                    orig = block.get('original_text', '')[:50]
                    sugg = block.get('suggested_fix', '')[:50]
                    print(f"  {i}. ID: {block.get('id')}")
                    print(f"     original: {orig}")
                    print(f"     suggestion: {sugg}")
                    print(f"     Confidence: {block.get('confidence', 0):.2f}")
                
                if len(garbled_blocks) > 5:
                    print(f"  ... English {len(garbled_blocks) - 5} Garbled text")
            
            if args.output:
                print(f"\nOutput path: {args.output}")
                print("Tip: Use --export-json to export in editable format for manual repair")
        else:
            print(f"✗ Processing failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)


if __name__ == "__main__":
    main()
